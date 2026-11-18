from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from .models import Family, Learner


def get_family(user):
    """The family this user owns or co-manages (one family per adult account)."""
    if not user.is_authenticated:
        return None
    fam = Family.objects.filter(owner=user).first()
    if fam:
        return fam
    membership = user.family_memberships.select_related("family").first()
    return membership.family if membership else None


def get_active_learner(request):
    family = get_family(request.user)
    learner_id = request.session.get("learner_id")
    if not family or not learner_id:
        return None
    return Learner.objects.filter(id=learner_id, family=family).first()


def family_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("core:login")
        family = get_family(request.user)
        if not family:
            messages.info(request, "Create your family account first.")
            return redirect("core:family_create")
        request.family = family
        return view(request, *args, **kwargs)
    return wrapper


def learner_required(view):
    @wraps(view)
    @family_required
    def wrapper(request, *args, **kwargs):
        learner = get_active_learner(request)
        if not learner:
            messages.info(request, "Choose who is learning.")
            return redirect("core:profiles")
        request.learner = learner
        return view(request, *args, **kwargs)
    return wrapper
