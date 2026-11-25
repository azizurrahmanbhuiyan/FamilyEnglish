from core.utils import get_active_learner


def studio_bar(request):
    """Streak, gems and XP for the top bar of every signed-in page."""
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {}
    learner = getattr(request, "learner", None) or get_active_learner(request)
    if not learner:
        return {}
    from growth import engine as growth

    from .engine import wallet
    try:
        info = growth.streak_info(learner)
        return {"bar": {"streak": info["streak"], "active_today": info["active_today"],
                        "gems": wallet(learner).gems, "xp": growth.totals(learner)["xp"]}}
    except Exception:  # never break a page because of the bar
        return {}
