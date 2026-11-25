"""Put lesson help text (meanings, tips, explanations) into the learner's language.

FamilyEnglish writes help text in English + Bangla. For any other language the English is translated
(world.translate). The English being learned — words, phrases, sentences to say — is never translated.
"""

from .middleware import current_lang, helper_lang
from .sources import js_strings
from .translate import many, text


def helper(en, bn, hl):
    if hl == "bn":
        return bn or ""
    if hl == "en":
        return ""
    return text(en, hl) if en else ""


def ui_pair(en, bn, ui):
    """[English, the same in the site language] for texts shown with t()/n() in JavaScript."""
    return [en, text(en, ui, bn)]


def localize_player(config, request):
    ui, hl = current_lang(request), helper_lang(request)
    config["lang"] = ui
    for it in config.get("items", []):
        it["bn"] = helper(it.get("text", ""), it.get("bn", ""), hl)
        it["tip_bn"] = text(it.get("tip_en", ""), ui, it.get("tip_bn", "")) if ui != "en" else it.get("tip_bn", "")
    lesson = config.get("lesson")
    if lesson:
        lesson["hello"] = [lesson["hello"][0], helper(lesson["hello"][0], lesson["hello"][1], hl)]
        lesson["rule"] = [lesson["rule"][0], helper(lesson["rule"][0], lesson["rule"][1], hl)]
        lesson["examples"] = [[e[0], helper(e[0], e[1], hl)] for e in lesson["examples"]]
    for line in config.get("lines", []):
        if hl != "bn":
            line["hint"] = ""
    if "prompt" in config:
        config["promptBn"] = helper(config["prompt"], config.get("promptBn", ""), hl)
    if ui not in ("en", "bn"):
        config["i18n"] = many(js_strings(), ui)
    return config


def localize_short(item, request):
    ui, hl = current_lang(request), helper_lang(request)
    item = dict(item)
    item["bn"] = helper(item.get("line", ""), item.get("bn", ""), hl)
    item["context_bn"] = text(item.get("context", ""), ui, item.get("context_bn", ""))
    return item


def js_i18n(request):
    ui = current_lang(request)
    return many(js_strings(), ui) if ui not in ("en", "bn") else {}
