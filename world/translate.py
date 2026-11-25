"""Show FamilyEnglish in any language.

    text(en, lang, bn=None)  -> the text in `lang`
      - en: English as written
      - bn: the Bangla written by FamilyEnglish
      - other languages: hand-written file world/locale/<lang>.json first, then saved translations
        (AI or edited in /admin). Text not translated yet is shown in English and saved as *pending*;
        `python manage.py translate_ui --pending` translates the pending ones with the AI key.

Translations are kept in memory and reloaded every few minutes, so new ones appear without a restart.
"""

import json
import time
from pathlib import Path

from django.db import IntegrityError, OperationalError, ProgrammingError

from .data import CODES

LOCALE_DIR = Path(__file__).resolve().parent / "locale"
RELOAD_SECONDS = 300
_tables = {}      # lang -> (loaded_at, {english: translation})
_queued = set()   # (lang, english) already saved as pending by this process


def _load(lang):
    table = {}
    f = LOCALE_DIR / f"{lang}.json"
    if f.exists():
        table.update(json.loads(f.read_text(encoding="utf-8")))
    try:
        from .models import UiText
        for src, txt, origin in UiText.objects.filter(lang=lang).exclude(text="").values_list("source", "text", "origin"):
            if origin == "manual" or src not in table:
                table[src] = txt
    except (OperationalError, ProgrammingError):  # tables not created yet (first migrate)
        pass
    _tables[lang] = (time.monotonic(), table)
    return table


def table(lang):
    hit = _tables.get(lang)
    if hit and time.monotonic() - hit[0] < RELOAD_SECONDS:
        return hit[1]
    return _load(lang)


def forget(lang=None):
    if lang:
        _tables.pop(lang, None)
    else:
        _tables.clear()


def _queue(lang, en):
    if (lang, en) in _queued or len(en) > 2000:
        return
    _queued.add((lang, en))
    try:
        from .models import UiText
        UiText.objects.get_or_create(lang=lang, key=UiText.key_for(en), defaults={"source": en})
    except (IntegrityError, OperationalError, ProgrammingError):
        pass


def text(en, lang, bn=None):
    if not en:
        return bn or en
    if lang == "bn":
        return bn or en
    if lang == "en" or lang not in CODES:
        return en
    t = table(lang).get(en)
    if t:
        return t
    _queue(lang, en)
    return en


def many(strings, lang):
    """{english: translation} for a list of strings (used to send UI words to JavaScript)."""
    return {s: text(s, lang) for s in strings if text(s, lang) != s}


def coverage(lang):
    """How much of the site is translated: (translated, pending)."""
    from .models import UiText
    done = len(table(lang))
    pending = UiText.objects.filter(lang=lang, text="").count()
    return done, pending
