from django import template

register = template.Library()

TABS = {
    "today": {("studio", "today"), ("learning", "today"), ("learning", "plan"), ("learning", "plan_new"), ("learning", "plan_day")},
    "coach": {("studio", n) for n in ("coach", "coach_detail", "coach_play", "sounds", "sound_drill", "analyzer", "rehearse")}
    | {("practice", n) for n in ("tutor", "tutor_history", "speaking", "writing")},
    "discover": {("studio", n) for n in ("discover", "dictionary", "my_words", "shorts")} | {("learning", "videos")},
    "progress": {("studio", n) for n in ("progress", "badges", "certificate")} | {("practice", "reports"), ("learning", "progress")},
    "more": {("studio", "more"), ("practice", "support"), ("practice", "refer"), ("practice", "tutorials")},
}


@register.simple_tag(takes_context=True)
def active_tab(context):
    request = context.get("request")
    m = getattr(request, "resolver_match", None)
    if not m:
        return ""
    key = (m.namespace, m.url_name)
    for tab, names in TABS.items():
        if key in names:
            return tab
    if m.namespace == "talk":
        return "talk"
    if m.namespace in ("growth",):
        return "progress"
    if m.namespace == "core":
        return "more"
    return "learn"


@register.filter
def pct(value, total):
    try:
        return round(int(value) * 100 / int(total)) if int(total) else 0
    except (TypeError, ValueError):
        return 0


@register.filter
def get(d, key):
    try:
        return d.get(key)
    except AttributeError:
        return None
