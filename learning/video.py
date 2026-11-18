"""Short topic videos, built from each lesson's own content.

Every lesson gets a 30–90 second narrated "video": a series of animated scenes that the
browser plays and reads aloud with its own voice (static/js/topic-video.js). No video files,
no hosting, no tracking. Change a lesson's words in /admin and its video changes with it.
"""

import re

SKILL_EMOJI = {
    "phonics": "🔤",
    "listening": "👂",
    "speaking": "🗣️",
    "reading": "📖",
    "writing": "✍️",
}

BLANK = re.compile(r"_{2,}")


def _spoken(text):
    """Text for the voice: drop phonics slashes, emoji and arrows so they are not read out."""
    text = re.sub(r"/([a-z]+)/", r"\1", text or "")
    text = re.sub(r"[^\w\s.,!?'’:;()\-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _word(item):
    """The plain word of a practice item ('☀️ sun' -> 'sun')."""
    return _spoken(item.prompt) or _spoken(item.answer)


def _sentences(text, limit=3):
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", text or "") if p.strip()]
    return parts[:limit]


def scene_ms(say, text=""):
    """Rough time a scene needs: about 2.4 spoken words a second, plus a pause to look."""
    words = len((say or text or "").split())
    return max(2600, int(words * 420) + 1400)


def build_scenes(lesson):
    level = lesson.module.level
    items = list(lesson.items.all())
    scenes = []

    eyebrow = f"Level {level.number} · {lesson.module.title}"
    if lesson.skill == "phonics" and lesson.focus:
        scenes.append(dict(kind="title", eyebrow=eyebrow, big=lesson.focus, text=lesson.title,
                           say="Let's learn a new sound!"))
        if lesson.action_hint:
            scenes.append(dict(kind="sound", eyebrow="Do the action", big=lesson.focus,
                               text=lesson.action_hint, say=_spoken(lesson.action_hint)))
    else:
        scenes.append(dict(kind="title", eyebrow=eyebrow, big=thumb_for(lesson, items),
                           text=lesson.title, say=f"Today's topic: {_spoken(lesson.title)}."))
        for s in _sentences(lesson.note_en):
            scenes.append(dict(kind="note", eyebrow="Learn", text=s, say=_spoken(s)))

    if lesson.activity == "quiz":
        for n, it in enumerate(items, 1):
            question = it.prompt
            asked = BLANK.sub("blank", question)
            scenes.append(dict(kind="question", eyebrow=f"Question {n}", big=it.picture,
                               text=question, say=_spoken(asked) + " Think!"))
            filled = BLANK.sub(it.answer, question) if BLANK.search(question) else f"{question} {it.answer}"
            answer_html = it.answer
            scenes.append(dict(kind="answer", eyebrow="Answer", big=it.picture, text=filled,
                               answer=answer_html, sub=it.meaning_bn,
                               say=_spoken(filled) if BLANK.search(question) else _spoken(it.answer)))
    else:
        words = []
        for it in items:
            w = _word(it)
            words.append(w)
            scenes.append(dict(kind="word", eyebrow="Listen and say", big=it.picture or "🔤",
                               text=w, sub=it.meaning_bn, say=f"{w}. ... {w}."))
        if len(words) > 1:
            scenes.append(dict(kind="recap", eyebrow="Say them all", text=" · ".join(words),
                               chips=[{"big": it.picture, "text": w} for it, w in zip(items, words)],
                               say="Now say them with me. " + ". ".join(words) + "."))

    outro_sub = lesson.home_task_en or "Then try the home task with your family."
    scenes.append(dict(kind="outro", eyebrow="Your turn", big="🎉", text="Now practise below!",
                       sub=outro_sub, say=f"Great job! Now it's your turn. {_spoken(outro_sub)}"))

    for s in scenes:
        s["ms"] = scene_ms(s.get("say"), s.get("text"))
    return scenes


def thumb_for(lesson, items=None):
    """The big picture on the video thumbnail."""
    if lesson.skill == "phonics" and lesson.focus:
        return lesson.focus
    items = list(lesson.items.all()) if items is None else items
    for it in items:
        if it.picture:
            return it.picture
    return SKILL_EMOJI.get(lesson.skill, "🎬")


def duration_seconds(lesson):
    return round(sum(s["ms"] for s in build_scenes(lesson)) / 1000)


def duration_label(seconds):
    return f"{seconds // 60}:{seconds % 60:02d}"
