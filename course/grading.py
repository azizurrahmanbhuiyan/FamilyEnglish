"""Marking engine shared by practice, self-tests, drills and the AI level test.

Every answer gets: right/wrong, a score, the correct answer, a word-by-word comparison that
shows the learner exactly what was wrong or missing, the lesson's explanation, extra
Bangla notes from the built-in checker and, for free answers, AI feedback when it is on.
"""

import json
import re
from difflib import SequenceMatcher

from practice import ai
from practice.feedback import check_writing, missed_words, speaking_score

SAY_PASS = 70      # % of the sentence heard in order
OPEN_PASS = 60

_QUOTES = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"'})
MECHANICS_HINTS = ("বড় হাতের", "space", "full stop", "capital")
SMALL_WORDS = {"that", "this", "with", "from", "have", "your", "there", "they", "them", "then", "what", "when",
               "were", "will", "would", "could", "please", "very", "just", "into", "about"}


def normalize(text, exact=False):
    text = (text or "").translate(_QUOTES).strip()
    text = re.sub(r"\s+", " ", text)
    if exact:
        return text
    text = text.lower()
    text = re.sub(r"[^\w\s']", "", text)  # drop punctuation, keep apostrophes and digits
    return re.sub(r"\s+", " ", text).strip()


def _tokens(text):
    return (text or "").translate(_QUOTES).split()


def word_diff(given, expected, exact=False):
    """[{'w': word, 's': 'ok' | 'wrong' | 'missing'}] comparing the learner's words with the answer."""
    g, e = _tokens(given), _tokens(expected)
    key = (lambda w: w) if exact else (lambda w: normalize(w))
    sm = SequenceMatcher(None, [key(w) for w in g], [key(w) for w in e])
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            out += [{"w": w, "s": "ok"} for w in g[i1:i2]]
        else:
            out += [{"w": w, "s": "wrong"} for w in g[i1:i2]]
            out += [{"w": w, "s": "missing"} for w in e[j1:j2]]
    return out


def _speech_notes(notes):
    """Speech-to-text has no capitals or punctuation, so drop those notes for spoken answers."""
    return [n for n in notes if not any(h in n for h in MECHANICS_HINTS)]


def _ai_open_feedback(item, given, level_hint=None):
    spoken = item.get("mode") == "speak"
    reply = ai.ask(
        "You mark one short answer from an English learner. "
        + ("It is a speech-to-text transcript: ignore punctuation, capitals and small recognition errors. "
           if spoken else "")
        + "Reply ONLY with JSON: {\"score\": 0-100, \"corrected\": \"<the answer with mistakes fixed>\", "
          "\"tips\": [\"<one short tip>\", …]} with at most 3 tips. Tip 1: one thing done well. "
          "Then the most important mistakes, each as: wrong → right, with a short reason in Bangla. "
          "Score fairly for the task and the learner's level: answering the task with clear, mostly "
          "correct English and enough length scores 70 or more.",
        [{"role": "user", "content": f"Task: {item.get('q')}\nMinimum words: {item.get('min', 20)}\n"
                                     f"Learner level (0-8): {level_hint if level_hint is not None else 'unknown'}\n"
                                     f"Answer: {given}"}],
        max_tokens=450)
    if not reply:
        return None
    try:
        data = json.loads(reply[reply.find("{"): reply.rfind("}") + 1])
        return {"score": max(0, min(100, int(data.get("score", 0)))),
                "corrected": str(data.get("corrected", ""))[:2000],
                "tips": [str(t) for t in data.get("tips", [])][:4]}
    except (ValueError, TypeError):
        return None


def check_item(item, given, use_ai=False, level_hint=None):
    """Mark one answer. Never raises; unknown item types count as wrong."""
    kind = item.get("t")
    given = (given or "").strip()[:2000]
    expected = item.get("a", "")
    res = {"ok": False, "score": 0, "expected": expected, "diff": [], "why": item.get("why", ""),
           "notes": [], "missed": [], "corrected": "", "ai": False, "kind": kind}

    if kind == "choose":
        res["ok"] = normalize(given) == normalize(expected)

    elif kind == "type":
        exact = item.get("exact", False)
        options = [expected] + list(item.get("accept", []))
        res["ok"] = any(normalize(given, exact) == normalize(o, exact) for o in options)
        if not res["ok"] and given:
            res["diff"] = word_diff(given, expected, exact)
            if len(given.split()) >= 2:
                _, notes = check_writing(given)
                if not exact:  # capitals and full stops are only marked in 'exact' items
                    notes = _speech_notes(notes)
                res["notes"] = notes[:3]

    elif kind == "say":
        res["score"] = speaking_score(expected, given)
        res["missed"] = missed_words(expected, given)
        # Small words are often lost by speech recognition, but a missed content word means the
        # sentence was not said correctly (e.g. 'brother' for 'mother').
        content_missed = [w for w in res["missed"] if len(w) > 3 and w not in SMALL_WORDS]
        res["ok"] = res["score"] >= SAY_PASS and not content_missed
        if given:
            res["diff"] = word_diff(given, expected)

    elif kind == "open":
        words = len(given.split())
        need = max(1, int(item.get("min", 20)))
        corrected, notes = check_writing(given) if given else ("", [])
        if item.get("mode") == "speak":
            notes = _speech_notes(notes)
        length_part = min(1.0, words / need) * 60
        accuracy_part = max(0, 40 - 10 * len(notes))
        res["score"] = round(length_part + accuracy_part) if given else 0
        res["corrected"] = corrected if notes else ""
        res["notes"] = notes[:4]
        if words < need and given:
            res["notes"].insert(0, f"আরও লিখুন/বলুন: অন্তত {need}টি শব্দ (এখন {words}টি)।")
        if use_ai and given:
            fb = _ai_open_feedback(item, given, level_hint)
            if fb:
                res.update(score=fb["score"], corrected=fb["corrected"], notes=fb["tips"], ai=True)
        res["ok"] = res["score"] >= OPEN_PASS
        res["expected"] = ""

    if kind in ("choose", "type") and res["ok"]:
        res["score"] = 100
    return res


def public_item(item):
    """What the browser may see before answering: no answers, choices shuffled by the caller."""
    out = {"t": item["t"], "q": item.get("q", ""), "say": item.get("say", ""),
           "qt": item.get("qt", ""), "min": item.get("min"), "mode": item.get("mode", "")}
    if item["t"] == "choose":
        out["opts"] = list(item.get("opts", []))
    if item["t"] == "say":
        out["a"] = item["a"]  # the sentence to say is the task itself
    return out
