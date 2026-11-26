from .utils import get_active_learner, get_family


def family_context(request):
    from django.conf import settings
    free = {"free_days": settings.FREE_TRIAL_DAYS}
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return free
    return {**free,
        "current_family": get_family(request.user),
        "current_learner": get_active_learner(request),
    }
