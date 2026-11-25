"""Sign-up for any country with a confirmation code, sign-in with a code, and the language picker."""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from core.models import Family

from . import otp
from .data import RTL, countries, guess, languages
from .forms import CodeForm, CodeLoginForm, GlobalSignupForm
from .middleware import current_lang
from .models import OneTimeCode, Profile
from .translate import text

User = get_user_model()
BACKEND = "django.contrib.auth.backends.ModelBackend"


def _country_data(lang):
    return {c["iso"]: {"dial": c["dial"], "example": c["example"], "lang": c["lang"], "flag": c["flag"]} for c in countries(lang)}


def signup(request):
    if request.user.is_authenticated:
        return redirect("core:profiles")
    lang = current_lang(request)
    ref = (request.GET.get("ref") or "").strip().upper()
    if ref:
        request.session["ref_code"] = ref
    inviter = Family.objects.filter(referral_code=request.session.get("ref_code") or "").first()
    iso, guessed_lang = guess(request)
    form = GlobalSignupForm(request.POST or None, lang=lang, initial={"country": iso, "language": lang or guessed_lang})
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.is_active = False  # until the code is confirmed
        user.save()
        d = form.cleaned_data
        Profile.objects.update_or_create(user=user, defaults={"country": d["country"], "phone": d["phone_e164"], "language": d["language"]})
        request.session["lang"] = d["language"]
        request.session["signup"] = {"user": user.pk, "family_name": d.get("family_name") or "", "relation": d.get("relation") or ""}
        _, places = otp.send_code(user, OneTimeCode.Purpose.SIGNUP, d["language"])
        request.session["otp_user"], request.session["otp_purpose"] = user.pk, "signup"
        messages.success(request, text("We sent a 6-digit code to", d["language"]) + " " + ", ".join(places))
        return redirect("world:verify")
    return render(request, "world/signup.html", {"form": form, "inviter": inviter, "extra_days": settings.REFERRAL_EXTRA_TRIAL_DAYS,
                                                 "country_data": _country_data(lang), "sms_on": otp.sms_enabled()})


def verify(request):
    """Type the 6-digit code (sign-up or sign-in)."""
    lang = current_lang(request)
    user = User.objects.filter(pk=request.session.get("otp_user")).first()
    purpose = request.session.get("otp_purpose", "signup")
    code_obj = OneTimeCode.objects.filter(user=user, purpose=purpose).first() if user else None
    form = CodeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if code_obj and code_obj.verify(form.cleaned_data["code"]):
            return _finish(request, user, purpose, lang)
        left = (OneTimeCode.MAX_ATTEMPTS - code_obj.attempts) if code_obj else 0
        if left > 0 and code_obj and code_obj.is_live:
            form.add_error("code", text("That code is not right. Tries left:", lang) + f" {left}")
        else:
            form.add_error("code", text("This code has expired. Ask for a new one.", lang))
    return render(request, "world/verify.html", {"form": form, "sent_to": code_obj.sent_to if code_obj else "",
                                                 "purpose": purpose, "has_user": bool(user)})


def resend(request):
    if request.method != "POST":
        return redirect("world:verify")
    lang = current_lang(request)
    user = User.objects.filter(pk=request.session.get("otp_user")).first()
    if user:
        ok, wait = otp.can_send(user)
        if ok:
            _, places = otp.send_code(user, request.session.get("otp_purpose", "signup"), lang)
            messages.success(request, text("We sent a new code to", lang) + " " + ", ".join(places))
        else:
            messages.warning(request, text("Please wait before asking for another code. Seconds:", lang) + f" {wait}")
    else:
        messages.success(request, text("If an account exists, we sent a new code.", lang))
    return redirect("world:verify")


def _finish(request, user, purpose, lang):
    p, _ = Profile.objects.get_or_create(user=user)
    p.email_verified = True
    if otp.sms_enabled() and p.phone:
        p.phone_verified = True
    p.save()
    if not user.is_active:
        user.is_active = True
        user.save(update_fields=["is_active"])
    login(request, user, backend=BACKEND)
    request.session["lang"] = p.language or lang
    for k in ("otp_user", "otp_purpose"):
        request.session.pop(k, None)
    if purpose == "signup":
        info = request.session.pop("signup", {}) or {}
        if not Family.objects.filter(owner=user).exists():
            inviter = Family.objects.filter(referral_code=request.session.get("ref_code") or "").first()
            Family.objects.create(name=info.get("family_name") or f"{user.first_name}'s family", owner=user,
                                  referred_by=inviter, country=p.country)
            request.session.pop("ref_code", None)
        messages.success(request, text("Welcome! Now add the people who will learn — children, parents or grandparents.", p.language))
        return redirect("core:learner_add")
    return redirect("core:profiles")


def login_code(request):
    """Sign in without a password: we send a code to the account's email (and mobile when SMS is on)."""
    if request.user.is_authenticated:
        return redirect("core:profiles")
    lang = current_lang(request)
    iso, _ = guess(request)
    form = CodeLoginForm(request.POST or None, lang=lang, initial={"country": iso})
    if request.method == "POST" and form.is_valid():
        user = form.user()
        request.session["otp_purpose"] = "login"
        request.session["otp_user"] = user.pk if user else None
        if user:
            ok, wait = otp.can_send(user)
            if ok:
                otp.send_code(user, OneTimeCode.Purpose.LOGIN, lang)
            else:
                messages.warning(request, text("Please wait before asking for another code. Seconds:", lang) + f" {wait}")
        messages.success(request, text("If an account exists, we sent a 6-digit code to its email.", lang))
        return redirect("world:verify")
    return render(request, "world/login_code.html", {"form": form, "country_data": _country_data(lang)})


def language(request):
    """Choose the site language — every language, searchable, with its own name."""
    lang = current_lang(request)
    nxt = request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"
    if not url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}) or reverse("world:language") in nxt:
        nxt = "/"
    return render(request, "world/language.html", {"langs": languages(lang), "current": lang, "next": nxt, "rtl": RTL})
