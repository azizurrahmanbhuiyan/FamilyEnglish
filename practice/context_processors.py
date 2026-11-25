from core.utils import get_active_learner

from .views import nav_counts


def practice_context(request):
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {}
    return {"nav": nav_counts(get_active_learner(request))}
