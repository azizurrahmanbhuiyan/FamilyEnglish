"""Password help for the phone app: forgot password (emailed code) and change password."""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from world import otp
from world.models import OneTimeCode, Profile

from .auth import family_of
from .views import LoginThrottle, _family, _learners

User = get_user_model()
SENT = "If an account exists, we sent a 6-digit code to its email."


def _user(email):
    email = (email or "").strip().lower()
    if "@" not in email:
        return None
    return User.objects.filter(Q(username=email) | Q(email__iexact=email)).order_by("-is_active", "pk").first()


def _check(password, user):
    try:
        validate_password(password, user)
    except ValidationError as e:
        return " ".join(e.messages)
    return ""


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([LoginThrottle])
def send_code(request):
    """POST {email} -> always the same answer, so nobody can test which emails have accounts."""
    user = _user(request.data.get("email"))
    if user:
        ok, wait = otp.can_send(user)
        if not ok:
            return Response({"detail": f"Please wait {wait} seconds before asking for another code."},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)
        otp.send_code(user, OneTimeCode.Purpose.LOGIN, request.data.get("lang") or "en")
    return Response({"detail": SENT})


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([LoginThrottle])
def reset(request):
    """POST {email, code, password} -> sets the new password and signs in: {token, family, learners}."""
    user = _user(request.data.get("email"))
    password = request.data.get("password") or ""
    problem = _check(password, user)  # before the code, so a weak password doesn't use the code up
    if problem:
        return Response({"detail": problem}, status=status.HTTP_400_BAD_REQUEST)
    code = OneTimeCode.objects.filter(user=user, purpose=OneTimeCode.Purpose.LOGIN).first() if user else None
    if not code or not code.verify(request.data.get("code")):
        return Response({"detail": "That code is not right or has expired. Ask for a new one."},
                        status=status.HTTP_400_BAD_REQUEST)
    user.set_password(password)
    user.is_active = True  # the emailed code proves the email, same as confirming sign-up
    user.save()
    Profile.objects.filter(user=user).update(email_verified=True)
    Token.objects.filter(user=user).delete()  # sign out old phones
    token = Token.objects.create(user=user)
    request.user = user
    family = family_of(request)
    return Response({"token": token.key, "family": _family(family), "learners": _learners(family)})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change(request):
    """POST {old, new} -> {detail, token}. Other phones are signed out."""
    user = request.user
    if not user.check_password(request.data.get("old") or ""):
        return Response({"detail": "Your current password is not right."}, status=status.HTTP_400_BAD_REQUEST)
    new = request.data.get("new") or ""
    problem = _check(new, user)
    if problem:
        return Response({"detail": problem}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(new)
    user.save()
    Token.objects.filter(user=user).delete()
    token = Token.objects.create(user=user)
    return Response({"detail": "Your new password is saved.", "token": token.key})
