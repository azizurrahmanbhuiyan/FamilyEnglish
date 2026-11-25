"""Find every English text the site shows, so a new language can be translated in one go."""

import re
from functools import lru_cache
from pathlib import Path

from django.conf import settings

ROOT = Path(settings.BASE_DIR)
TR_TAG = re.compile(r"""\{%\s*tr\s+(["'])(.+?)\1\s+(["'])(.*?)\3\s*%\}""", re.S)
JS_T = re.compile(r"""\bt\(\s*"((?:[^"\\]|\\.)+)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*\)""")
PY_TEXT = re.compile(r"""\btext\(\s*"((?:[^"\\]|\\.)+)"\s*,""")


def _unescape(s):
    return s.replace('\\"', '"').replace("\\'", "'").replace("\\n", "\n")


@lru_cache(maxsize=1)
def template_strings():
    out = []
    for f in sorted((ROOT / "templates").rglob("*.html")):
        for m in TR_TAG.finditer(f.read_text(encoding="utf-8")):
            out.append(m.group(2))
    return out


@lru_cache(maxsize=1)
def js_strings():
    out = []
    for f in sorted((ROOT / "static" / "js").glob("*.js")):
        for m in JS_T.finditer(f.read_text(encoding="utf-8")):
            out.append(_unescape(m.group(1)))
    return out


@lru_cache(maxsize=1)
def python_strings():
    out = []
    for f in sorted((ROOT / "world").glob("*.py")):
        for m in PY_TEXT.finditer(f.read_text(encoding="utf-8")):
            out.append(_unescape(m.group(1)))
    return out


@lru_cache(maxsize=1)
def content_strings():
    """English help texts inside lessons (they have Bangla versions written by FamilyEnglish)."""
    from studio.content import coaches as C
    from studio.content import grammar as G
    from studio.content import ielts as I
    from studio.content import sounds as S
    from studio.content import units as U
    out = []
    for u in U.UNITS:
        out += [u["title"], u["desc"], u["outcome"]]
        out += [U.parse_word(w)["text"] for w in u["words"]]
        out += [p[0] for p in u["phrases"]]
    for g in G.LESSONS:
        out += [g["title"], g["sub"], g["hello"][0], g["rule"][0]] + [e[0] for e in g["examples"]]
    for c in C.COACHES:
        out += [c["title"], c["desc"]] + [s["title"] for s in c["scenarios"]]
    for t in I.TOPICS:
        out.append(t["title"])
    for en, _bn in S.SOUNDS.values():
        out.append(en)
    for _code, en, _bn in G.LEVELS:
        out.append(en)
    from studio.content import pronunciation as PR
    from studio.content import stories as ST
    for p in PR.LESSONS:
        out += [p["title"], p["sub"], p["hello"][0], p["rule"][0]] + [e[0] for e in p["examples"]]
    out += [s[2] for s in PR.STAGES]
    for st in ST.STORIES:
        out += [st["title"], st["focus"]] + [v[1] for v in st["vocab"]] + [ln[0] for ln in st["lines"]]
    for p in PR.LESSONS:
        out += [d[0] for d in p["drill"]]
    from studio import shorts as SH
    out += [t[1] for t in SH.TOPICS]
    return out


def all_strings():
    seen, out = set(), []
    for s in template_strings() + js_strings() + python_strings() + content_strings():
        s = s.strip()
        if s and s not in seen and "{{" not in s and "{%" not in s:
            seen.add(s)
            out.append(s)
    return out
