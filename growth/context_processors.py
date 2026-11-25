from django.utils.functional import SimpleLazyObject

from core.utils import get_active_learner


def growth_context(request):
    from django.conf import settings

    from world.middleware import current_lang
    lang = current_lang(request)

    ctx = {"lang": lang, "messenger_url": settings.MESSENGER_URL}
    if getattr(request, "user", None) and request.user.is_authenticated:
        learner = get_active_learner(request)
        if learner:
            from . import engine
            ctx["xp_panel"] = SimpleLazyObject(lambda: engine.xp_panel(learner))
    return ctx
