"""Pick the site language for each request: chosen language -> account language -> browser language."""

from .data import RTL, guess, is_language, native_name


def current_lang(request):
    session = getattr(request, "session", None)
    if session is None:
        return "en"
    lang = session.get("lang")
    if lang and is_language(lang):
        return lang
    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated:
        from .models import Profile
        lang = Profile.objects.filter(user=user).values_list("language", flat=True).first()
    if not lang or not is_language(lang):
        _, lang = guess(request)
    session["lang"] = lang
    return lang


def helper_lang(request):
    """Language for meanings and explanations inside lessons: the site language, except that English-site
    users in Bangladesh keep the Bangla meanings they had before."""
    lang = current_lang(request)
    if lang != "en":
        return lang
    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated:
        from .models import Profile
        country = Profile.objects.filter(user=user).values_list("country", flat=True).first() or "BD"
        return "bn" if country == "BD" else "en"
    return "bn"


def world_context(request):
    lang = current_lang(request)
    return {"lang_dir": "rtl" if lang in RTL else "ltr", "lang_native": native_name(lang)}
