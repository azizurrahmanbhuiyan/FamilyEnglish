"""Every language and country FamilyEnglish offers, with native names, flags and dial codes.

Names come from the Unicode CLDR data (Babel), so a learner who chooses Hindi sees country names in
Hindi. Dial codes, number checks and example numbers come from Google's libphonenumber (phonenumbers).
"""

from functools import lru_cache

import phonenumbers
from babel import Locale
from babel.languages import get_official_languages

# 112 languages. Codes are what we store and put in the URL / session.
CODES = ("en bn hi ur ar es fr pt id zh-Hans ru tr ne vi af am as az be bg bho bs ca ceb ckb cs cy da de dv el et eu fa "
         "fi fil ga gl gu ha he hr ht hu hy ig is it ja jv ka kk km kn ko kok ku ky lb lo lt lv mai mg mi mk ml mn mr ms "
         "mt my nb nl ny om or pa pl ps qu ro rw sa sat sd si sk sl sn so sq sr st sv sw ta te tg th ti tk tn tt ug uk "
         "uz xh yi yo zh-Hant zu").split()

# Written by hand for the main screens (the rest is translated by AI and saved). English and Bangla are complete.
HAND_WRITTEN = ("en", "bn", "hi", "ur", "ar", "es", "fr", "pt", "id", "zh-Hans", "ru", "tr", "ne", "vi")
RTL = {"ar", "fa", "he", "ps", "sd", "ug", "ur", "yi", "ckb", "dv"}


def babel_code(code):
    return code.replace("-", "_")


def is_language(code):
    return code in CODES


@lru_cache(maxsize=None)
def languages(ui="en"):
    """[(code, native name, name in the UI language)], English and Bangla first, then by English name."""
    ui_loc = Locale.parse(babel_code(ui if ui in CODES else "en"))
    out = []
    for c in CODES:
        loc = Locale.parse(babel_code(c))
        native = loc.get_display_name(babel_code(c)) or c
        out.append((c, native[:1].upper() + native[1:], loc.get_display_name(ui_loc) or native, loc.get_display_name("en")))
    head = [x for x in out if x[0] in ("en", "bn")]
    rest = sorted([x for x in out if x[0] not in ("en", "bn")], key=lambda x: x[3])
    return [(c, n, u) for c, n, u, _ in head + rest]


def native_name(code):
    return next((n for c, n, _ in languages("en") if c == code), code)


def english_name(code):
    try:
        return Locale.parse(babel_code(code)).get_display_name("en")
    except Exception:  # pragma: no cover
        return code


def flag(iso2):
    return "".join(chr(0x1F1E6 + ord(ch) - ord("A")) for ch in iso2.upper()) if len(iso2) == 2 else "🌐"


@lru_cache(maxsize=None)
def countries(ui="en"):
    """[{iso, name, flag, dial, example, lang}] for every country with a phone dial code, sorted by name."""
    names = Locale.parse(babel_code(ui if ui in CODES else "en")).territories
    out = []
    for iso in sorted(phonenumbers.SUPPORTED_REGIONS):
        if iso in ("001",) or not iso.isalpha():
            continue
        dial = phonenumbers.country_code_for_region(iso)
        ex = phonenumbers.example_number_for_type(iso, phonenumbers.PhoneNumberType.MOBILE)
        example = phonenumbers.format_number(ex, phonenumbers.PhoneNumberFormat.NATIONAL) if ex else ""
        out.append({"iso": iso, "name": names.get(iso, iso), "flag": flag(iso), "dial": dial, "example": example,
                    "lang": default_language(iso)})
    import locale as _l  # noqa: F401  (sorting by the shown name is good enough for every script)
    return sorted(out, key=lambda c: c["name"])


@lru_cache(maxsize=None)
def default_language(iso):
    for code in get_official_languages(iso, de_facto=True):
        code = {"zh_Hans": "zh-Hans", "zh_Hant": "zh-Hant", "zh": "zh-Hans", "no": "nb", "pt_PT": "pt"}.get(code, code)
        if code in CODES:
            return code
    return "en"


def country(iso, ui="en"):
    return next((c for c in countries(ui) if c["iso"] == (iso or "").upper()), None)


def normalise_phone(national, iso):
    """'01712-345678', 'BD' -> '+8801712345678', or None if it is not a valid mobile/fixed number there."""
    try:
        n = phonenumbers.parse(national, (iso or "").upper())
    except phonenumbers.NumberParseException:
        return None
    if not phonenumbers.is_valid_number(n) or phonenumbers.region_code_for_number(n) != (iso or "").upper():
        return None
    return phonenumbers.format_number(n, phonenumbers.PhoneNumberFormat.E164)


def guess(request):
    """Best guess of (country, language) from the browser's language header, e.g. 'bn-BD,bn;q=0.9'."""
    header = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
    iso, lang = None, None
    for part in header.split(","):
        tag = part.split(";")[0].strip()
        if not tag:
            continue
        bits = tag.replace("_", "-").split("-")
        base = bits[0].lower()
        if not lang:
            if base == "zh":
                lang = "zh-Hant" if any(b.upper() in ("TW", "HK", "HANT", "MO") for b in bits[1:]) else "zh-Hans"
            elif base in CODES:
                lang = base
        if not iso:
            for b in bits[1:]:
                if len(b) == 2 and b.isalpha() and b.upper() in phonenumbers.SUPPORTED_REGIONS:
                    iso = b.upper()
    iso = request.META.get("HTTP_CF_IPCOUNTRY") or iso or "BD"
    if iso not in phonenumbers.SUPPORTED_REGIONS:
        iso = "BD"
    return iso, lang or "en"
