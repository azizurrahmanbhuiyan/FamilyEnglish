"""Scoring and progress for the speaking studio: tries, finished lessons, gems, scores, journey, badges."""

import difflib
import re
import secrets
from datetime import timedelta

from django.db.models import Avg, Sum
from django.utils import timezone

from .content import grammar as G
from .content import ielts as I
from .content import units as U
from .models import Attempt, Certificate, LessonDone, Wallet

CEFR = [("A1", 0), ("A2", 20), ("B1", 40), ("B2", 60), ("C1", 75), ("C2", 90)]
FILLERS = {"um", "uh", "er", "erm", "hmm", "like", "basically", "actually"}
LINKERS = {"because", "however", "although", "though", "so", "therefore", "moreover", "while", "whereas",
           "which", "who", "if", "unless", "since", "but", "also", "instead", "example", "finally", "firstly"}


# ------------------------------------------------------------------ text helpers

def norm(text):
    text = (text or "").lower().replace("’", "'").replace("‘", "'")
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def words(text):
    return norm(text).split()


def similarity(target, said):
    """0–100: how much of the target the learner said, word by word, in order."""
    t, s = words(target), words(said)
    if not t or not s:
        return 0
    m = difflib.SequenceMatcher(None, t, s)
    matched = sum(b.size for b in m.get_matching_blocks())
    recall = matched / len(t)
    precision = matched / len(s)
    return round(100 * (0.75 * recall + 0.25 * precision))


def speech_score(target, said, confidence=None):
    sim = similarity(target, said)
    if confidence is not None and 0 < confidence <= 1 and sim >= 60:
        sim = round(sim * (0.8 + 0.2 * confidence))
    return max(0, min(100, sim))


def word_marks(target, said):
    """For each target word: True if it was heard. Used to colour words green or red."""
    t_raw = target.split()
    t = [norm(w) for w in t_raw]
    s = words(said)
    heard = set()
    m = difflib.SequenceMatcher(None, t, s)
    for b in m.get_matching_blocks():
        heard.update(range(b.a, b.a + b.size))
    return [{"w": w, "ok": i in heard} for i, w in enumerate(t_raw)]


def check_typed(answer, accepted):
    a = norm(answer)
    return any(a == norm(x) for x in accepted)


def check_pattern(answer, pattern):
    return bool(re.search(pattern, (answer or "").lower().replace("’", "'").strip()))


def analyse_speech(transcript, seconds, target_wpm=120, min_words=40):
    """Band-style feedback for free speaking: fluency, vocabulary range, grammar range, length."""
    w = words(transcript)
    n = len(w)
    seconds = max(1, int(seconds or 0))
    wpm = round(n * 60 / seconds) if n else 0
    fillers = sum(1 for x in w if x in FILLERS) + norm(transcript).count("you know")
    content = [x for x in w if x not in FILLERS]
    unique = len(set(content)) / len(content) if content else 0
    long_words = sum(1 for x in content if len(x) >= 7)
    linkers = sorted({x for x in content if x in LINKERS})

    fluency = 0 if not n else max(0, min(100, 100 - abs(wpm - target_wpm) * 0.7 - fillers * 4))
    vocab = 0 if not n else max(0, min(100, unique * 80 + min(30, long_words * 3)))
    grammar = 0 if not n else max(0, min(100, 35 + len(linkers) * 9))
    length = max(0, min(100, n * 100 / min_words))
    overall = round((fluency + vocab + grammar + length) / 4)
    tips = []
    if n < min_words:
        tips.append(("Say more: add a reason and an example.", "আরও বলুন: একটি কারণ ও একটি উদাহরণ যোগ করুন।"))
    if wpm and wpm < target_wpm - 30:
        tips.append(("Try to keep going without long pauses.", "লম্বা বিরতি ছাড়া বলে যাওয়ার চেষ্টা করুন।"))
    if wpm > target_wpm + 40:
        tips.append(("Slow down a little so every word is clear.", "একটু ধীরে বলুন, যাতে প্রতিটি শব্দ পরিষ্কার হয়।"))
    if fillers > 2:
        tips.append(("Use fewer fillers like 'um' and 'like'. Pause silently instead.", "'um', 'like' কম বলুন; দরকার হলে চুপ করে থামুন।"))
    if len(linkers) < 3:
        tips.append(("Join ideas with because, although, however, for example.", "because, although, however, for example দিয়ে ধারণা জুড়ুন।"))
    if unique < .55 and n > 20:
        tips.append(("Use a wider range of words — avoid repeating the same ones.", "একই শব্দ বারবার না বলে নানা শব্দ ব্যবহার করুন।"))
    if not tips:
        tips.append(("Excellent! Clear, linked and varied. Try a harder topic next.", "চমৎকার! এবার আরও কঠিন বিষয় চেষ্টা করুন।"))
    return {"words": n, "wpm": wpm, "seconds": seconds, "fillers": fillers, "unique": round(unique * 100),
            "long_words": long_words, "linkers": linkers, "fluency": round(fluency), "vocab": round(vocab),
            "grammar": round(grammar), "length": round(length), "overall": overall, "band": ielts_band(overall), "tips": tips}


# ------------------------------------------------------------------ records

def record(learner, kind, key, item="", said="", score=0, seconds=0, wpm=0, ai_used=False):
    return Attempt.objects.create(learner=learner, kind=kind, key=key[:80], item=(item or "")[:200], said=said or "",
                                  score=max(0, min(100, int(score or 0))), seconds=min(int(seconds or 0), 3600),
                                  wpm=min(int(wpm or 0), 400), ai_used=ai_used)


def wallet(learner):
    return Wallet.objects.get_or_create(learner=learner)[0]


def add_gems(learner, n):
    w = wallet(learner)
    w.gems += n
    w.earned += n
    w.save(update_fields=["gems", "earned"])
    return w


def finish(learner, key, title, score):
    """Mark a studio lesson finished. First time: XP and gems. Returns (lesson_done, first_time)."""
    from growth import engine as growth

    done, created = LessonDone.objects.get_or_create(learner=learner, key=key[:80],
                                                     defaults={"title": title[:160], "score": score})
    if not created and score > done.score:
        done.score = score
        done.save(update_fields=["score"])
    if created:
        growth.award(learner, 20 + score // 5, "Studio lesson", key=f"studio:{key}"[:80])
        add_gems(learner, 5 if score >= 90 else 2)
        issue_certificates(learner)
    return done, created


def done_keys(learner):
    return set(LessonDone.objects.filter(learner=learner).values_list("key", flat=True))


# ------------------------------------------------------------------ units, grammar, IELTS progress

def unit_key(unit_slug, n):
    return f"unit:{unit_slug}:{n}"


def unit_progress(unit, done):
    n = sum(1 for t in U.LESSON_TYPES if unit_key(unit["slug"], t[0]) in done)
    return {"done": n, "total": len(U.LESSON_TYPES), "percent": round(n * 100 / len(U.LESSON_TYPES))}


def next_unit_lesson(unit, done):
    for t in U.LESSON_TYPES:
        if unit_key(unit["slug"], t[0]) not in done:
            return t
    return None


def grammar_key(slug):
    return f"grammar:{slug}"


def ielts_key(band, topic, n):
    return f"ielts:{band}:{topic}:{n}"


def level_done(level, done):
    lessons = G.by_level(level)
    return sum(1 for g in lessons if grammar_key(g["slug"]) in done), len(lessons)


# ------------------------------------------------------------------ scores and journey

def _avg(qs):
    v = qs.aggregate(a=Avg("score"))["a"]
    return round(v) if v is not None else None


def _recent(learner, kinds, n=60):
    ids = list(Attempt.objects.filter(learner=learner, kind__in=kinds).values_list("id", flat=True)[:n])
    return Attempt.objects.filter(id__in=ids)


def scores(learner):
    """Five skill scores (0–100, or None when not measured yet), overall, CEFR and IELTS estimate."""
    from practice.models import LEARNED_BOX, CardReview

    pron = _avg(_recent(learner, ["repeat", "short"]))
    flu = _avg(_recent(learner, ["speech", "ielts", "convo", "coach"], 30))
    gram = _avg(_recent(learner, ["grammar"]))
    learned = CardReview.objects.filter(learner=learner, box__gte=LEARNED_BOX).count()
    word_tries = _avg(_recent(learner, ["words"]))
    vocab = None
    if learned or word_tries is not None:
        vocab = min(100, round(learned / 30 + (word_tries or 0) * 0.4))
    listen = None
    try:
        from course.path import start_bands
        _, levels, _ = start_bands(learner)
        if levels.get("listening"):
            listen = min(100, round(levels["listening"] * 12.5))
    except Exception:  # pragma: no cover - course data missing
        pass
    listen_tries = _avg(_recent(learner, ["listen"]))
    if listen_tries is not None:
        listen = listen_tries if listen is None else round((listen + listen_tries) / 2)
    parts = [("pronunciation", "Pronunciation", "উচ্চারণ", pron), ("fluency", "Fluency", "সাবলীলতা", flu),
             ("listening", "Listening", "শোনা", listen), ("grammar", "Grammar", "ব্যাকরণ", gram),
             ("vocabulary", "Vocabulary", "শব্দভান্ডার", vocab)]
    measured = [p[3] for p in parts if p[3] is not None]
    overall = round(sum(measured) / len(measured)) if measured else None
    return {"parts": [{"key": k, "en": en, "bn": bn, "score": v} for k, en, bn, v in parts],
            "overall": overall, "cefr": cefr(overall) if overall is not None else None,
            "ielts": ielts_band(overall) if overall is not None else None, "measured": len(measured)}


def cefr(score):
    level = "A1"
    for name, low in CEFR:
        if score >= low:
            level = name
    return level


def ielts_band(score):
    return max(3.0, min(9.0, round((2 + score * 0.07) * 2) / 2))


def journey(learner, sc=None):
    """'Your journey': current CEFR level, next level and progress between them."""
    sc = sc or scores(learner)
    if sc["overall"] is None:
        return {"current": "A1", "next": "A2", "percent": 0, "measured": False}
    s = sc["overall"]
    names = [c[0] for c in CEFR]
    lows = [c[1] for c in CEFR] + [100]
    i = names.index(sc["cefr"])
    if i == len(names) - 1:
        return {"current": "C2", "next": "C2", "percent": 100, "measured": True}
    pct = round((s - lows[i]) * 100 / (lows[i + 1] - lows[i]))
    return {"current": names[i], "next": names[i + 1], "percent": max(0, min(100, pct)), "measured": True}


def pentagon(sc, size=300):
    """SVG points for the five-sided score chart (grid rings and the learner's shape)."""
    import math
    cx = cy = size / 2
    r = size / 2 - 62
    n = 5

    def pt(i, frac):
        a = -math.pi / 2 + i * 2 * math.pi / n
        return round(cx + r * frac * math.cos(a), 1), round(cy + r * frac * math.sin(a), 1)

    rings = [" ".join(f"{x},{y}" for x, y in (pt(i, f) for i in range(n))) for f in (.25, .5, .75, 1)]
    shape = " ".join(f"{x},{y}" for x, y in (pt(i, max(.04, (p["score"] or 0) / 100)) for i, p in enumerate(sc["parts"])))
    labels = []
    for i, p in enumerate(sc["parts"]):
        x, y = pt(i, 1.28)
        labels.append({"x": x, "y": y, "en": p["en"], "bn": p["bn"], "score": p["score"]})
    axes = [pt(i, 1) for i in range(n)]
    return {"size": size, "cx": cx, "cy": cy, "rings": rings, "shape": shape, "labels": labels, "axes": axes}


# ------------------------------------------------------------------ time, week, history

def learning_seconds(learner):
    from course.models import CourseProgress
    from learning.models import Progress

    studio = Attempt.objects.filter(learner=learner).aggregate(s=Sum("seconds"))["s"] or 0
    lessons = CourseProgress.objects.filter(learner=learner).count() + Progress.objects.filter(learner=learner).count()
    return studio + lessons * 240


def lessons_count(learner):
    from course.models import CourseProgress
    from learning.models import Progress

    return (LessonDone.objects.filter(learner=learner).count() + CourseProgress.objects.filter(learner=learner, passed=True).count()
            + Progress.objects.filter(learner=learner).count())


def week(learner, today=None):
    """Last 7 days: minutes and XP per day, and whether the learner was active."""
    from growth.models import XPEvent

    today = today or timezone.localdate()
    out = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        start = timezone.make_aware(timezone.datetime(d.year, d.month, d.day))
        end = start + timedelta(days=1)
        secs = Attempt.objects.filter(learner=learner, created_at__gte=start, created_at__lt=end).aggregate(s=Sum("seconds"))["s"] or 0
        xp = XPEvent.objects.filter(learner=learner, created_at__gte=start, created_at__lt=end).aggregate(s=Sum("amount"))["s"] or 0
        out.append({"day": d, "label": d.strftime("%a")[:2], "minutes": round(secs / 60), "xp": xp, "active": xp > 0 or secs > 0,
                    "today": d == today})
    top = max([x["xp"] for x in out] + [1])
    for x in out:
        x["height"] = round(x["xp"] * 100 / top)
    return out


def streak_week(learner, today=None):
    """Saturday-to-Friday dots for the current Bangladeshi week."""
    from growth import engine as growth

    today = today or timezone.localdate()
    start = today - timedelta(days=(today.weekday() - 5) % 7)
    active = growth.active_days(learner, since=start)
    return [{"day": start + timedelta(days=i), "label": (start + timedelta(days=i)).strftime("%a"),
             "on": (start + timedelta(days=i)) in active, "today": start + timedelta(days=i) == today,
             "future": start + timedelta(days=i) > today} for i in range(7)]


# ------------------------------------------------------------------ today

def today_tasks(learner):
    """Three tasks a day, like a coach would set: a sound drill, new words and a conversation."""
    done = done_keys(learner)
    today = timezone.localdate()
    done_today = set(LessonDone.objects.filter(learner=learner, finished_at__date=today).values_list("key", flat=True))
    tasks = []
    for n, label, label_bn, icon in ((2, "Sound drill", "উচ্চারণ অনুশীলন", "wave"),
                                     (1, "New words", "নতুন শব্দ", "cards"),
                                     (4, "Conversation", "কথোপকথন", "chat")):
        today_one = next((k for k in done_today if k.startswith("unit:") and k.endswith(f":{n}")), None)
        if today_one:
            slug = today_one.split(":")[1]
            tasks.append({"n": n, "label": label, "label_bn": label_bn, "icon": icon, "unit": U.BY_SLUG.get(slug),
                          "done": True})
            continue
        unit = next((u for u in U.UNITS if unit_key(u["slug"], n) not in done), U.UNITS[-1])
        tasks.append({"n": n, "label": label, "label_bn": label_bn, "icon": icon, "unit": unit, "done": False})
    return tasks


def current_unit(learner, done=None):
    done = done if done is not None else done_keys(learner)
    for u in U.UNITS:
        if unit_progress(u, done)["done"] < len(U.LESSON_TYPES):
            return u
    return U.UNITS[-1]


# ------------------------------------------------------------------ badges and certificates

STUDIO_BADGES = [
    ("sound10", "🔊", "Sound starter", "উচ্চারণে শুরু", "Get 80%+ on 10 repeat-after-me words", "good_repeats", 10),
    ("sound100", "🎧", "Clear speaker", "স্পষ্ট বক্তা", "Get 80%+ on 100 repeat-after-me tries", "good_repeats", 100),
    ("chat5", "💬", "Chatterbox", "গল্পবাজ", "Finish 5 conversations", "convos", 5),
    ("units5", "🧭", "Explorer", "অভিযাত্রী", "Finish 5 Learn units", "units", 5),
    ("grammar10", "📚", "Grammar fan", "ব্যাকরণপ্রেমী", "Finish 10 grammar coach lessons", "grammar", 10),
    ("speech5", "🎙️", "Speech star", "বক্তৃতা তারকা", "Use the speech analyzer 5 times", "speeches", 5),
    ("ielts5", "🎓", "Exam ready", "পরীক্ষার জন্য প্রস্তুত", "Answer 5 IELTS questions", "ielts", 5),
    ("shorts20", "🎬", "Shorts star", "শর্টস তারকা", "Say back 20 short videos with 70%+", "shorts", 20),
    ("words25", "🔖", "Word saver", "শব্দ সঞ্চয়ী", "Save 25 words to My Words", "bookmarks", 25),
]


def studio_stats(learner):
    done = done_keys(learner)
    return {
        "good_repeats": Attempt.objects.filter(learner=learner, kind="repeat", score__gte=80).count(),
        "convos": sum(1 for k in done if k.startswith("unit:") and k.endswith(":4")) + sum(1 for k in done if k.startswith("coach:")),
        "units": sum(1 for u in U.UNITS if unit_progress(u, done)["done"] == len(U.LESSON_TYPES)),
        "grammar": sum(1 for k in done if k.startswith("grammar:")),
        "speeches": Attempt.objects.filter(learner=learner, kind="speech").count(),
        "ielts": Attempt.objects.filter(learner=learner, kind="ielts").count(),
        "bookmarks": learner.bookmarks.count(),
        "shorts": Attempt.objects.filter(learner=learner, kind="short", score__gte=70).values("key").distinct().count(),
    }


def all_badges(learner):
    from growth import engine as growth

    out = growth.badges(learner)
    stats = studio_stats(learner)
    for key, icon, name, name_bn, desc, stat, target in STUDIO_BADGES:
        now = stats.get(stat, 0)
        out.append({"key": key, "icon": icon, "name": name, "name_bn": name_bn, "desc": desc,
                    "now": min(now, target), "target": target, "earned": now >= target,
                    "percent": min(100, round(now * 100 / target))})
    return out


def _issue(learner, code, title, title_bn):
    if Certificate.objects.filter(learner=learner, code=code).exists():
        return None
    number = f"FE-{timezone.localdate().year}-{secrets.token_hex(3).upper()}"
    return Certificate.objects.create(learner=learner, code=code, title=title, title_bn=title_bn, number=number)


def issue_certificates(learner):
    """Give a certificate when a whole grammar level, a level of units or an IELTS course is finished."""
    done = done_keys(learner)
    for level, name, name_bn in G.LEVELS:
        d, total = level_done(level, done)
        if total and d == total:
            _issue(learner, f"grammar-{level.lower()}", f"Grammar {level} — {name}", f"ব্যাকরণ {level} — {name_bn}")
    for level in ("A1", "A2", "B1"):
        units = [u for u in U.UNITS if u["level"] == level]
        if units and all(unit_progress(u, done)["done"] == len(U.LESSON_TYPES) for u in units):
            _issue(learner, f"everyday-{level.lower()}", f"Everyday English {level}", f"দৈনন্দিন ইংরেজি {level}")
    for band in I.BANDS:
        keys = [ielts_key(band, t["slug"], n) for t in I.units_for(band) for n, *_ in I.LESSONS]
        if keys and all(k in done for k in keys):
            _issue(learner, f"ielts-{band}", f"IELTS Speaking — Band {band} course", f"IELTS স্পিকিং — ব্যান্ড {band} কোর্স")
