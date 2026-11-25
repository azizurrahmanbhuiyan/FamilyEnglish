"""Short videos: watch one line, then say it back.

Two kinds of shorts share one feed:
  anim   FamilyEnglish's own animated shorts, made from the lesson content (unit phrases and
         conversations, grammar examples, IELTS model answers, coach role-plays). The browser
         animates the scene and reads the line in a British voice, highlighting each word.
  video  A real YouTube clip approved in /admin that has a "say line" (the line spoken in it).
"""

import random
from functools import lru_cache

from django.utils import timezone

from .content import coaches as C
from .content import grammar as G
from .content import ielts as I
from .content import units as U

FREE_PER_DAY = 5
PAGE = 12

TOPICS = [
    ("all", "For you", "আপনার জন্য", "✨"),
    ("home", "Family & home", "পরিবার ও বাড়ি", "🏠"),
    ("food", "Food & shopping", "খাবার ও কেনাকাটা", "🥭"),
    ("school", "School & fun", "স্কুল ও আনন্দ", "🎒"),
    ("out", "Out & about", "বাইরে", "🛺"),
    ("work", "Work & life", "কাজ ও জীবন", "💼"),
    ("grammar", "Grammar", "ব্যাকরণ", "🧩"),
    ("ielts", "IELTS", "IELTS", "🎓"),
    ("videos", "Real videos", "আসল ভিডিও", "🎬"),
]
TOPIC_KEYS = {t[0] for t in TOPICS}

UNIT_TOPIC = {
    "hello": "home", "family": "home", "home": "home", "birthday": "home", "routine": "home", "feelings": "home",
    "bazaar": "food", "restaurant": "food", "shopping": "food",
    "school": "school", "time": "school", "hobbies": "school", "story": "school",
    "transport": "out", "directions": "out", "weather": "out", "village": "out", "eid": "out", "weekend": "out",
    "bank": "work", "jobs": "work", "phone": "work", "plans": "work", "doctor": "work",
}
COACH_TOPIC = {"everyday": "out", "travel": "out", "doctor": "work", "school-meeting": "school", "storytelling": "school"}

# background gradients per topic (two colours)
SKY = {"home": ("#ff8a5c", "#c2367a"), "food": ("#f7b733", "#e0532f"), "school": ("#3fd3a8", "#1d6fd8"),
       "out": ("#4facfe", "#6a3df0"), "work": ("#7f7fd5", "#2b2a7a"), "grammar": ("#a26bff", "#3d2bbf"),
       "ielts": ("#2fe0b5", "#145a96"), "videos": ("#222244", "#111122")}
SPEAKERS = ["👩🏽", "👨🏽", "👵🏽", "👴🏽", "🧒🏽", "👧🏽", "👩🏽‍🏫", "👨🏽‍💼", "👩🏽‍⚕️", "🧑🏽‍🍳"]


def _short(sid, topic, line, bn="", scene="🎬", context="", context_bn="", speaker="", kind="anim", **extra):
    return {"id": sid, "topic": topic, "line": line, "bn": bn, "scene": scene, "context": context, "context_bn": context_bn,
            "speaker": speaker or SPEAKERS[sum(map(ord, sid)) % len(SPEAKERS)], "kind": kind,
            "sky": SKY.get(topic, SKY["out"]), **extra}


@lru_cache(maxsize=1)
def animated():
    out = []
    for u in U.UNITS:
        topic = UNIT_TOPIC.get(u["slug"], "home")
        for i, (text, _sound, bn) in enumerate(u["phrases"]):
            out.append(_short(f"u.{u['slug']}.p{i}", topic, text, bn, u["emoji"], u["title"], u["title_bn"]))
        for i, (bot, reply, _hint) in enumerate(u["convo"]):
            out.append(_short(f"u.{u['slug']}.b{i}", topic, bot, "", u["emoji"], u["title"], u["title_bn"]))
            out.append(_short(f"u.{u['slug']}.r{i}", topic, reply, "", u["emoji"], u["title"], u["title_bn"]))
    for g in G.LESSONS:
        for i, (en, bn) in enumerate(g["examples"]):
            out.append(_short(f"g.{g['slug']}.{i}", "grammar", en, bn, g["icon"], f"{g['level']} · {g['title']}", g["title_bn"]))
    for t in I.TOPICS:
        for i, sentence in enumerate(t["model"]):
            out.append(_short(f"i.{t['slug']}.{i}", "ielts", sentence, "", t["emoji"], f"Part {t['part']} · {t['title']}", t["title_bn"]))
    for c in C.COACHES:
        for s in c["scenarios"]:
            topic = COACH_TOPIC.get(c["slug"], "work")
            for i, (bot, reply) in enumerate(s["lines"]):
                out.append(_short(f"c.{c['slug']}.{s['slug']}.{i}", topic, reply, "", c["icon"], s["title"], s["title_bn"]))
    return out


def videos():
    from learning.models import VideoClip
    out = []
    for clip in VideoClip.objects.visible().exclude(say_line="").order_by("-id")[:200]:
        out.append(_short(f"v.{clip.pk}", "videos", clip.say_line, clip.say_line_bn, "🎬", clip.title or "Real video", "আসল ভিডিও",
                          speaker="🎬", kind="video", youtube=clip.youtube_id, start=clip.start, end=clip.end))
    return out


def by_id(sid):
    if sid.startswith("v."):
        return next((s for s in videos() if s["id"] == sid), None)
    return next((s for s in animated() if s["id"] == sid), None)


def feed(learner, topic="all", offset=0, limit=PAGE):
    """Shorts for this learner: not-yet-mastered first, in a fresh order each day; real videos mixed in."""
    from .models import Attempt

    topic = topic if topic in TOPIC_KEYS else "all"
    mastered = set(Attempt.objects.filter(learner=learner, kind="short", score__gte=70).values_list("key", flat=True))
    vids = videos()
    if topic == "videos":
        pool = vids
    elif topic == "all":
        pool = list(animated())
    else:
        pool = [s for s in animated() if s["topic"] == topic]
    rnd = random.Random(learner.pk * 100003 + timezone.localdate().toordinal())
    fresh = [s for s in pool if f"short:{s['id']}" not in mastered]
    again = [s for s in pool if f"short:{s['id']}" in mastered]
    rnd.shuffle(fresh)
    rnd.shuffle(again)
    items = fresh + again
    if topic == "all" and vids:  # a real video after every 4 animated shorts
        mixed, vi = [], 0
        for i, s in enumerate(items):
            mixed.append(s)
            if i % 4 == 3 and vi < len(vids):
                mixed.append(vids[vi])
                vi += 1
        items = mixed
    page = items[offset:offset + limit]
    return [{**s, "mastered": f"short:{s['id']}" in mastered} for s in page], offset + limit < len(items), len(items)


def done_today(learner):
    from .models import Attempt
    start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    return Attempt.objects.filter(learner=learner, kind="short", created_at__gte=start).values("key").distinct().count()


def counts():
    out = {t[0]: 0 for t in TOPICS}
    for s in animated():
        out[s["topic"]] += 1
        out["all"] += 1
    return out
