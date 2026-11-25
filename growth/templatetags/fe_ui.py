from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def tr(context, en, bn=""):
    """{% tr "English text" "বাংলা লেখা" %} — shows the text in the chosen site language.

    English and Bangla are written by FamilyEnglish; every other language comes from world.translate
    (hand-written files, then AI translations saved in the database)."""
    from world.translate import text
    return text(en, context.get("lang") or "en", bn)


@register.filter
def get_item(mapping, key):
    try:
        return mapping.get(key)
    except AttributeError:
        return None


# ------------------------------------------------------------------ icons
# Simple hand-made line icons (24×24, drawn with the current text colour) used instead of emoji in
# menus, buttons and cards. Emoji stay only where they are content for children (animals, pictures).
ICONS = {
    "home": '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9.5h13V10"/><path d="M10 19.5v-5h4v5"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2.5"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/><path d="M8 13.5h2M14 13.5h2M8 16.5h2"/>',
    "test": '<rect x="5.5" y="4.5" width="13" height="16" rx="2"/><path d="M9.5 4.5v-1h5v1"/><path d="m9 13 2 2 4-4.5"/>',
    "compass": '<circle cx="12" cy="12" r="8.5"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
    "ear": '<path d="M7 9.5a5 5 0 1 1 10 0c0 3-3 4-3 6.5a3 3 0 0 1-5.5 1.6"/><path d="M10 10a2 2 0 1 1 3 1.7"/>',
    "speak": '<path d="M4.5 18.5 6 15a7 7 0 1 1 3 2.6z"/><path d="M9 10.5h6M9 13h4"/>',
    "book": '<path d="M12 6.5c-2-1.5-5-2-8-1.5v13c3-.5 6 0 8 1.5 2-1.5 5-2 8-1.5V5c-3-.5-6 0-8 1.5z"/><path d="M12 6.5v13"/>',
    "pen": '<path d="m15 4.5 4.5 4.5L9 19.5H4.5V15z"/><path d="m12.5 7 4.5 4.5"/>',
    "puzzle": '<path d="M9 4.5h3.5a1.8 1.8 0 1 1 3 1.5h0v3.5h3.5v4h-1a1.8 1.8 0 1 0 0 3.5h1v2.5H5V16h1a1.8 1.8 0 1 0 0-3.5H5v-3h4z"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r=".8" fill="currentColor"/>',
    "letters": '<path d="m3.5 17 3-9 3 9M4.5 14h4"/><path d="M12.5 8v9h2.5a2.2 2.2 0 0 0 0-4.5h-2.5M12.5 12.5H15a2.2 2.2 0 0 0 0-4.5h-2.5"/><path d="M21 9.5a2.8 2.8 0 1 0 0 6"/>',
    "library": '<path d="M4.5 4.5h3v15h-3zM9.5 4.5h3v15h-3z"/><path d="m14.5 5.2 2.9-.8 3.6 14.4-2.9.7z"/>',
    "family": '<circle cx="8" cy="7.5" r="2.5"/><circle cx="16.5" cy="9" r="2"/><path d="M3.5 19c0-3 2-5 4.5-5s4.5 2 4.5 5"/><path d="M13 19c.2-2.4 1.6-4 3.5-4s3.3 1.6 3.5 4"/>',
    "film": '<rect x="3.5" y="5.5" width="17" height="13" rx="2.5"/><path d="m10.5 9.5 4 2.5-4 2.5z"/>',
    "cards": '<rect x="7.5" y="4" width="11" height="14.5" rx="2" transform="rotate(8 13 11)"/><rect x="4.5" y="6" width="11" height="14.5" rx="2"/>',
    "headphones": '<path d="M4.5 15v-3a7.5 7.5 0 0 1 15 0v3"/><rect x="3.5" y="14" width="4" height="6" rx="1.5"/><rect x="16.5" y="14" width="4" height="6" rx="1.5"/>',
    "keyboard": '<rect x="2.5" y="6.5" width="19" height="11" rx="2"/><path d="M6 10h.01M9 10h.01M12 10h.01M15 10h.01M18 10h.01M7.5 14h9"/>',
    "check": '<path d="M9 3.5h6M10 3.5v5L5 18a1.6 1.6 0 0 0 1.4 2.5h11.2A1.6 1.6 0 0 0 19 18l-5-9.5v-5"/><path d="M7.5 14.5h9"/>',
    "chat": '<path d="M5 18.5V7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H8.5z"/><path d="M9 10h6M9 12.5h3.5"/>',
    "mic": '<rect x="9" y="3.5" width="6" height="11" rx="3"/><path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3"/>',
    "chart": '<path d="M4 20h16"/><path d="M7 16.5v-5M12 16.5v-9M17 16.5v-6"/>',
    "flame": '<path d="M12 21c-3.6 0-6-2.4-6-5.6C6 11 11 9 10.5 3.5c3 1.8 4.5 4.5 4 7.5 1-.5 1.7-1.5 2-2.5 1.2 1.6 1.5 3.4 1.5 5 0 4.2-2.5 7.5-6 7.5z"/>',
    "trophy": '<path d="M8 4.5h8v5a4 4 0 0 1-8 0z"/><path d="M8 6.5H5a3 3 0 0 0 3 4M16 6.5h3a3 3 0 0 1-3 4"/><path d="M12 13.5V17M8.5 20h7M9.5 17h5v3h-5z"/>',
    "user": '<circle cx="12" cy="8.5" r="3.5"/><path d="M5 20c.5-3.5 3.3-5.5 7-5.5s6.5 2 7 5.5"/>',
    "swap": '<path d="M4.5 8.5h13l-3-3M19.5 15.5h-13l3 3"/>',
    "gift": '<rect x="4" y="9" width="16" height="11" rx="1.5"/><path d="M3 9h18M12 9v11"/><path d="M12 9c-1.5-3.5-5-4-5-1.5S10 9 12 9c1.5-3.5 5-4 5-1.5S14 9 12 9"/>',
    "help": '<circle cx="12" cy="12" r="8.5"/><path d="M9.6 9.5a2.5 2.5 0 1 1 3.4 2.3c-.7.3-1 .8-1 1.5v.4"/><circle cx="12" cy="16.6" r=".6" fill="currentColor"/>',
    "bell": '<path d="M6.5 16.5v-5a5.5 5.5 0 0 1 11 0v5l1.5 2H5z"/><path d="M10 20.5a2 2 0 0 0 4 0"/>',
    "bulb": '<path d="M9 17.5h6M10 20.5h4"/><path d="M8.5 14.5a5.5 5.5 0 1 1 7 0c-.7.6-1 1.4-1 2.3v.2h-5v-.2c0-.9-.3-1.7-1-2.3z"/>',
    "wallet": '<rect x="3.5" y="6.5" width="17" height="12.5" rx="2"/><path d="M3.5 10h17"/><path d="M15.5 14.5h2"/>',
    "signout": '<path d="M14 4.5H6.5v15H14"/><path d="M10.5 12h10m-3-3 3 3-3 3"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="m6 6 12 12M18 6 6 18"/>',
    "star": '<path d="m12 4 2.4 5 5.3.7-3.9 3.7 1 5.3L12 16.2l-4.8 2.5 1-5.3-3.9-3.7 5.3-.7z"/>',
    "bolt": '<path d="M13 3.5 5.5 13.5h6l-1 7 7.5-10h-6z"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
    "unlock": '<rect x="5" y="10.5" width="14" height="10" rx="2"/><path d="M8 10.5V8a4 4 0 0 1 7.7-1.5"/>',
    "arrow": '<path d="M5 12h14m-5-5 5 5-5 5"/>',
    "repeat": '<path d="M4.5 11V9.5a3 3 0 0 1 3-3h11l-3-3M19.5 13v1.5a3 3 0 0 1-3 3h-11l3 3"/>',
    "link": '<path d="M10 14a3.5 3.5 0 0 0 5 0l3-3a3.5 3.5 0 0 0-5-5l-1 1"/><path d="M14 10a3.5 3.5 0 0 0-5 0l-3 3a3.5 3.5 0 0 0 5 5l1-1"/>',
    "external": '<path d="M13.5 4.5h6v6M19.5 4.5 11 13"/><path d="M17.5 14v5.5h-13v-13H10"/>',
    "play": '<path d="M8 5.5v13l10.5-6.5z"/>',
    "leaf": '<path d="M5 19c0-8 5-13.5 14.5-14-0.5 9.5-6 14.5-14 14z"/><path d="M5 19 13 11"/>',
    "seed": '<path d="M12 20.5v-7"/><path d="M12 13.5c0-4-3-6.5-7-6.5 0 4 3 6.5 7 6.5zM12 12c0-3.5 2.5-6 6.5-6 0 3.6-2.6 6-6.5 6z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6 7 7M17 17l1.4 1.4M5.6 18.4 7 17M17 7l1.4-1.4"/>',
    "grandparent": '<circle cx="11" cy="6.5" r="2.5"/><path d="M6.5 20.5 8 12.5c.5-2 4.5-2 5 0l1 4"/><path d="M17.5 12v8.5M17.5 12a2 2 0 0 0-2-2"/>',
    "school": '<path d="M3 9.5 12 5l9 4.5-9 4.5z"/><path d="M7 11.5V16c3 2 7 2 10 0v-4.5"/><path d="M21 9.5V15"/>',
    "gem": '<path d="M7 4.5h10l3.5 5L12 20.5 3.5 9.5z"/><path d="M3.5 9.5h17M9.5 4.5 8 9.5l4 11 4-11-1.5-5"/>',
    "sparkle": '<path d="M12 3.5c.6 4.3 2.7 6.4 7 7-4.3.6-6.4 2.7-7 7-.6-4.3-2.7-6.4-7-7 4.3-.6 6.4-2.7 7-7z"/><path d="M18.5 3.5v3M17 5h3"/>',
    "coach": '<rect x="3.5" y="6.5" width="17" height="11" rx="3.5"/><circle cx="9" cy="12" r="1.3" fill="currentColor"/><circle cx="15" cy="12" r="1.3" fill="currentColor"/><path d="M12 6.5v-2"/>',
    "progress": '<path d="M4 19.5h16"/><path d="m4.5 15 4.5-4.5 3.5 3 7-7"/><path d="M15 6.5h4.5V11"/>',
    "volume": '<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z"/><path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11"/>',
    "snail": '<path d="M3.5 18.5h15a2.5 2.5 0 0 0 2.5-2.5V13"/><circle cx="12" cy="12.5" r="5"/><path d="M12 12.5a2 2 0 1 1 2-2"/><path d="M18.5 13V8.5M21 13V9"/>',
    "bookmark": '<path d="M6.5 4.5h11v16l-5.5-4-5.5 4z"/><path d="M15.5 2.5v4M13.5 4.5h4"/>',
    "listen-self": '<circle cx="9" cy="8.5" r="3.5"/><path d="M3 20c.5-3.5 3-5.5 6-5.5s5.5 2 6 5.5"/><path d="M16 6a3.5 3.5 0 0 1 0 5M18.5 3.5a7 7 0 0 1 0 10"/>',
    "info": '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5"/><circle cx="12" cy="7.8" r=".7" fill="currentColor"/>',
    "retry": '<path d="M19.5 12a7.5 7.5 0 1 1-2.2-5.3"/><path d="M19.5 4.5v4h-4"/>',
    "skip": '<path d="M5.5 5.5v13l9-6.5z"/><path d="M18 5.5v13"/>',
    "wave": '<path d="M4 12h.01M8 9v6M12 6v12M16 9v6M20 12h.01"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/>',
    "chevron": '<path d="m9.5 5.5 6.5 6.5-6.5 6.5"/>',
    "back": '<path d="M19 12H5m6-6-6 6 6 6"/>',
    "stop": '<rect x="6.5" y="6.5" width="11" height="11" rx="2.5"/>',
    "grid": '<rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/>',
    "check-circle": '<circle cx="12" cy="12" r="8.5"/><path d="m8.5 12.3 2.3 2.2 4.7-5"/>',
}


@register.simple_tag
def icon(name, cls="ico"):
    from django.utils.html import format_html, mark_safe
    body = ICONS.get(name, ICONS["star"])
    return format_html('<svg class="{}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
                       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>', cls, mark_safe(body))
