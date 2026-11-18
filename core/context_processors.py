from .utils import get_active_learner, get_family


def family_context(request):
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {}
    return {
        "current_family": get_family(request.user),
        "current_learner": get_active_learner(request),
    }
