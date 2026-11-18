import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def md_lite(text):
    """Escape, then turn **bold** into <strong> and blank-line blocks into paragraphs."""
    if not text:
        return ""
    html = escape(text)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    paras = [p.strip().replace("\n", "<br>") for p in html.split("\n\n") if p.strip()]
    return mark_safe("".join(f"<p>{p}</p>" for p in paras))


@register.filter
def split_choices(text):
    return [c.strip() for c in (text or "").split(",") if c.strip()]


@register.filter
def stars(n):
    return "⭐" * int(n or 0)
