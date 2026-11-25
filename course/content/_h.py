"""Tiny helpers that keep the lesson content files short and readable.

Item types
  choose  multiple choice. "say" = text the browser reads aloud first (listening).
  type    type the answer (gap fill, dictation, fix the sentence, put words in order).
          exact=True also checks capital letters and punctuation.
  say     say a sentence into the microphone (or type it if the browser cannot listen).
  open    a free answer, written or spoken; checked by the AI coach or the built-in checker.
"""


def C(q, a, *wrong, why="", qt="", say=""):
    return {"t": "choose", "q": q, "a": a, "opts": [a, *wrong], "why": why, "qt": qt, "say": say}


def T(q, a, why="", qt="", say="", accept=(), exact=False):
    return {"t": "type", "q": q, "a": a, "why": why, "qt": qt, "say": say,
            "accept": list(accept), "exact": exact}


def S(text, why="", qt="spk_sentence"):
    return {"t": "say", "q": "Say this sentence.", "a": text, "why": why, "qt": qt}


def O(q, why="", qt="wr_free", min=20, mode="write"):
    return {"t": "open", "q": q, "why": why, "qt": qt, "min": min, "mode": mode}


def L(slug, band, order, title, title_bn, goal, note_en, note_bn, tip_bn="", examples=(),
      errors=(), passage="", passage_title="", video="", practice=(), test=(), minutes=15):
    return {
        "slug": slug, "band": band, "order": order, "title": title, "title_bn": title_bn,
        "goal": goal, "note_en": note_en, "note_bn": note_bn, "guidance_bn": tip_bn,
        "examples": list(examples),
        "errors": [{"avoid": a, "use": u, "why": w} for a, u, w in errors],
        "passage": passage, "passage_title": passage_title, "video_query": video,
        "practice": list(practice), "selftest": list(test), "minutes": minutes,
    }
