"""Talk lessons: start a conversation, reply (AI or scripted), hints, translation and the lesson report.

The website (talk.views) and the phone app (api.talk) both call these functions, so they always agree.

AI is optional. Without FE_AI_API_KEY every lesson still works: role-plays follow their four
scripted lines, daily talks and Read-and-talk use our own questions, and the report shows the
numbers we can measure (words used, new words, fluency, pronunciation) without corrections.
"""

import json
import random
import re

from django.conf import settings
from django.utils import timezone

from practice import ai
from studio import engine as E
from studio.models import Attempt

from .content import roleplays as RP
from .content import topics as T
from .models import Article, TalkProfile, TalkSession

TALK_AI_DAILY = int(getattr(settings, "TALK_AI_DAILY_LIMIT", 60))
MAX_TURNS = 12  # learner turns before the tutor wraps up
STOP = set("""a an the i you he she it we they me him her us them my your his its our their is am are was were be been
being do does did have has had to of in on at for with and or but so if then than that this these those there here
what when where who why how yes no not ok okay oh um uh er like just very really too also can could will would shall
should may might must from up down out about into over again some any all more most much many one two""".split())


# ------------------------------------------------------------------ profile and limits

def profile(learner):
    return TalkProfile.objects.get_or_create(learner=learner)[0]


def ai_used_today(learner):
    start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    return Attempt.objects.filter(learner=learner, key__startswith="talkai:", created_at__gte=start).count()


def ai_ok(learner):
    return ai.enabled() and ai_used_today(learner) < TALK_AI_DAILY


def _count_ai(learner, session, what):
    E.record(learner, "coach", f"talkai:{session.pk}", what, "", 0)


def minutes_today(learner):
    start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    secs = sum(TalkSession.objects.filter(learner=learner, created_at__gte=start).values_list("seconds", flat=True))
    return round(secs / 60)


# ------------------------------------------------------------------ what is free

def daily_used_today(learner):
    return TalkSession.objects.filter(learner=learner, kind="daily", created_at__date=timezone.localdate()).exists()


def can_open(family, learner, kind, ref=""):
    """Free families: one daily talk a day, three role-plays and three Read-and-talk articles."""
    if family.has_full_access:
        return True
    if kind == "daily":
        return not daily_used_today(learner)
    if kind == "roleplay":
        return ref in RP.FREE
    if kind == "article":
        return ref in T.FREE_SEEDS
    return False


# ------------------------------------------------------------------ the daily topic

def daily_topic(learner, prof=None):
    """Today's category and opening question, from the learner's interests (same all day)."""
    prof = prof or profile(learner)
    keys = [k for k in prof.interests if k in T.BY_KEY] or [c["key"] for c in T.CATEGORIES]
    rnd = random.Random(f"{learner.pk}:{timezone.localdate():%Y%m%d}")
    cat = T.BY_KEY[rnd.choice(keys)]
    return cat, rnd.choice(cat["openers"])


# ------------------------------------------------------------------ articles

def article(slug, create=True):
    """A Read-and-talk article as a dict, or None. Topic ideas are written by AI once and saved."""
    cat, a = T.seed(slug)
    if a:
        return {**a, "category": cat["key"], "seed": True}
    row = Article.objects.filter(slug=slug).first()
    if row:
        return {"slug": row.slug, "title": row.title, "level": row.level, "body": row.body, "questions": row.questions,
                "words": row.words, "category": row.category, "seed": False}
    cat, title = T.topic(slug)
    if not cat or not create or not ai.enabled():
        return None
    text = ai.ask(
        "You write short reading texts for English learners. Write ONE original article (170–230 words, 3–4 short "
        "paragraphs, CEFR B1, British spelling) on the title given. Make it friendly, factual and suitable for families "
        "and children; use a Bangladeshi example if it fits. Do not copy any existing article. Reply with JSON only: "
        '{"title": "...", "body": "paragraphs separated by \\n\\n", "questions": ["3 open questions to discuss"], '
        '"words": [["word", "simple meaning"], ...3 words]}',
        [{"role": "user", "content": title}], max_tokens=900)
    data = _json(text)
    if not data or not data.get("body"):
        return None
    row, _ = Article.objects.get_or_create(slug=slug, defaults={
        "category": cat["key"], "title": str(data.get("title") or title)[:160], "level": 3, "body": str(data["body"])[:4000],
        "questions": [str(q)[:200] for q in (data.get("questions") or [])][:4] or cat["openers"],
        "words": [[str(w[0])[:40], str(w[1])[:120]] for w in (data.get("words") or []) if isinstance(w, list) and len(w) >= 2][:5]})
    return article(slug, create=False)


def library(paid):
    """Categories with their articles for the Read-and-talk page."""
    have = set(Article.objects.values_list("slug", flat=True))
    out = []
    for c in T.CATEGORIES:
        items = [{"slug": c["seed"]["slug"], "title": c["seed"]["title"], "ready": True,
                  "free": c["seed"]["slug"] in T.FREE_SEEDS, "seed": True}]
        for i, title in enumerate(c["topics"]):
            slug = T.topic_slug(c["key"], i)
            items.append({"slug": slug, "title": title, "ready": slug in have or ai.enabled(), "free": False, "seed": False})
        for it in items:
            it["locked"] = not paid and not it["free"]
        out.append({"key": c["key"], "emoji": c["emoji"], "title": c["title"], "title_bn": c["title_bn"], "items": items})
    return out


# ------------------------------------------------------------------ starting a talk

def start(learner, kind, ref="", setting="", persona=""):
    """Create a session and its opening line. Returns the session, or None if ref is unknown."""
    prof = profile(learner)
    name = learner.name
    if kind == "daily":
        cat, q = daily_topic(learner, prof)
        s = TalkSession(learner=learner, kind=kind, ref=cat["key"], title=f"Daily talk · {cat['title']}",
                        setting=f"A friendly chat about {cat['title'].lower()}", persona="a warm English tutor called Doel",
                        goal="Talk for a few minutes and share your own ideas.")
        opener = f"Hi {name}! Let's talk about {cat['title'].lower()} today. {q}"
    elif kind == "roleplay":
        r = RP.BY_SLUG.get(ref)
        if not r:
            return None
        s = TalkSession(learner=learner, kind=kind, ref=ref, title=r["title"], setting=r["setting"], persona=r["persona"], goal=r["goal"])
        opener = r["lines"][0][0]
    elif kind == "custom":
        setting, persona = setting.strip()[:280], persona.strip()[:180]
        if not setting or not persona:
            return None
        s = TalkSession(learner=learner, kind=kind, ref="custom", title=f"My role-play: {setting[:60]}", setting=setting,
                        persona=persona, goal="Practise this situation in your own words.")
        opener = None
    elif kind == "article":
        a = article(ref)
        if not a:
            return None
        s = TalkSession(learner=learner, kind=kind, ref=ref, title=f"Read and talk · {a['title']}"[:160],
                        setting=f"Talking about the article '{a['title']}'", persona="a curious English tutor called Doel",
                        goal="Share your opinion about the article.")
        opener = f"So, {name}, you've read '{a['title']}'. {a['questions'][0]}"
    else:
        return None
    s.save()
    if opener is None:
        opener = _ai_reply(learner, s, prof, []) if ai_ok(learner) else None
        opener = opener or f"Hello! I'm {persona}. How can I help you today?"
    s.script_step = 1
    s.messages = [{"role": "assistant", "content": opener}]
    s.save(update_fields=["messages", "script_step"])
    return s


# ------------------------------------------------------------------ replying

def _system(s, prof):
    level = dict((n, label) for n, label, *_ in T.LEVELS).get(prof.level, "Elementary")
    correct = {"always": "If the learner makes any grammar or word mistake, add one short tip in brackets at the end, "
                         "like (Tip: say 'I went', not 'I go yesterday').",
               "big": "Only if the learner makes a big mistake that changes the meaning, add one short tip in brackets at the end, "
                      "like (Tip: …). Ignore small mistakes.",
               "end": "Do not correct mistakes during the talk; corrections come in the report later."}.get(prof.correct, "")
    if s.kind in ("roleplay", "custom"):
        role = (f"Role-play. You are {s.persona}. Setting: {s.setting}. The learner's goal: {s.goal} "
                "Stay in your role and react naturally to what the learner says.")
    else:
        role = (f"You are {s.persona}, having a friendly spoken conversation. Topic: {s.setting}. "
                "Show interest, share a short thought of your own sometimes, and ask one follow-up question each time.")
    return (f"{role} The learner's level is {level} (1–5 scale: {prof.level}); use words and sentence length that suit "
            f"this level. Reply in 1–3 short spoken sentences of natural British English, no lists, no emojis, and end with a "
            f"question so the learner keeps talking. {correct} "
            f"If the learner writes in Bangla or says they don't understand, explain more simply in English.")


def _ai_reply(learner, s, prof, history):
    msgs = [{"role": m["role"], "content": str(m["content"])[:500]} for m in history if m.get("role") in ("user", "assistant")][-14:]
    if not msgs or msgs[0]["role"] != "user":
        msgs = [{"role": "user", "content": "(The conversation starts. Say your first line.)"}] + msgs
    text = ai.ask(_system(s, prof), msgs, max_tokens=180)
    if text:
        _count_ai(learner, s, "reply")
    return text


def _split_tip(text):
    m = re.search(r"\((?:Tip|tip)\s*:\s*(.+?)\)\s*$", text or "")
    if not m:
        return text, ""
    return text[:m.start()].strip(), m.group(1).strip()


def _scripted(s):
    """Next scripted line when AI is off (or the daily AI allowance is used up)."""
    if s.kind == "roleplay":
        lines = RP.BY_SLUG[s.ref]["lines"]
        if s.script_step < len(lines):
            return lines[s.script_step][0]
    elif s.kind == "article":
        a = article(s.ref, create=False)
        qs = (a or {}).get("questions", [])
        if s.script_step < len(qs):
            return "Thanks for sharing. " + qs[s.script_step]
    elif s.kind == "daily":
        cat = T.BY_KEY.get(s.ref)
        others = [q for q in (cat["openers"] if cat else []) if q not in s.messages[0]["content"]]
        if s.script_step - 1 < len(others):
            return "That's interesting! " + others[s.script_step - 1]
    return None


def reply(learner, s, text, confidence=None, seconds=0):
    """The learner said or typed text. Returns {reply, tip, done}."""
    text = (text or "").strip()[:600]
    if not text:
        return {"reply": "", "tip": "", "done": False}
    conf = confidence if isinstance(confidence, (int, float)) and 0 < confidence <= 1 else None
    s.messages.append({"role": "user", "content": text, **({"conf": round(conf, 2)} if conf else {})})
    s.seconds = min(s.seconds + max(0, min(int(seconds or 0), 300)), 7200)
    E.record(learner, "coach", f"talk:{s.pk}", s.title, text, min(95, 55 + len(E.words(text)) * 4), seconds)
    turns = len(s.user_turns)
    prof = profile(learner)
    answer, tip, done = None, "", False
    if turns >= MAX_TURNS:
        answer, done = "This was a great talk! Tap 'Finish' to see your lesson report.", True
    elif ai_ok(learner):
        answer = _ai_reply(learner, s, prof, s.messages)
        answer, tip = _split_tip(answer) if answer else (None, "")
    if not answer:
        answer = _scripted(s)
        s.script_step += 1
        if not answer:
            answer, done = "Well done — you finished this conversation! Tap 'Finish' to see your report.", True
    s.messages.append({"role": "assistant", "content": answer, **({"tip": tip} if tip else {})})
    s.save(update_fields=["messages", "seconds", "script_step"])
    return {"reply": answer, "tip": tip, "done": done}


def hint(learner, s):
    """Something the learner could say next."""
    if s.kind == "roleplay" and not ai_ok(learner):
        lines = RP.BY_SLUG[s.ref]["lines"]
        i = max(0, min(s.script_step - 1, len(lines) - 1))
        return lines[i][1]
    if ai_ok(learner):
        last = s.messages[-1]["content"] if s.messages else ""
        prof = profile(learner)
        text = ai.ask(f"Suggest ONE short, natural answer (max 15 words) the learner could say next. Learner level {prof.level} of 5. "
                      f"Situation: {s.setting}. Reply with the sentence only.",
                      [{"role": "user", "content": f"The other person said: {last}"}], max_tokens=60)
        if text:
            _count_ai(learner, s, "hint")
            return text.strip().strip('"')
    return "Start with: I think… / In my opinion… / For example…"


def translate(learner, s, text):
    """Bangla translation of a tutor line (AI only)."""
    text = (text or "").strip()[:400]
    if not text or not ai_ok(learner):
        return None
    out = ai.ask("Translate the English text into simple, natural Bangla. Reply with the translation only.",
                 [{"role": "user", "content": text}], max_tokens=200)
    if out:
        _count_ai(learner, s, "translate")
    return out


# ------------------------------------------------------------------ the report

def _json(text):
    if not text:
        return None
    m = re.search(r"\{.*\}", text, re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except ValueError:
        return None


def _content_words(text):
    return [w for w in E.words(text) if len(w) >= 3 and w not in STOP and not w.isdigit()]


def words_known(learner, before=None):
    """Every content word this learner has used in earlier talks."""
    qs = TalkSession.objects.filter(learner=learner)
    if before is not None:
        qs = qs.exclude(pk=before.pk).filter(created_at__lt=before.created_at)
    seen = set()
    for msgs in qs.values_list("messages", flat=True):
        for m in msgs or []:
            if m.get("role") == "user":
                seen.update(_content_words(m.get("content", "")))
    return seen


def finish(learner, s):
    """Build (once) and return the lesson report."""
    if s.report:
        return s.report
    turns = s.user_turns
    said = " ".join(m["content"] for m in turns)
    used = _content_words(said)
    unique = sorted(set(used), key=used.index)
    known = words_known(learner, before=s)
    new = [w for w in unique if w not in known][:12]
    confs = [m["conf"] for m in turns if m.get("conf")]
    n_words = len(E.words(said))
    per_turn = n_words / len(turns) if turns else 0
    pron = round(sum(confs) / len(confs) * 100) if confs else None
    fluency = round(max(0, min(100, 30 + per_turn * 6))) if turns else 0
    best = max(turns, key=lambda m: len(E.words(m["content"])))["content"] if turns else ""
    report = {"turns": len(turns), "words": n_words, "unique": len(unique), "new_words": new,
              "vocab_total": len(known | set(unique)), "pronunciation": pron, "fluency": fluency, "grammar": None,
              "best": best, "takeaway": "", "takeaway_bn": "", "better": [], "ai": False, "minutes": round(s.seconds / 60)}
    if turns and ai_ok(learner):
        convo = "\n".join(("LEARNER: " if m["role"] == "user" else "TUTOR: ") + m["content"] for m in s.messages)[-6000:]
        data = _json(ai.ask(
            "You review an English learner's spoken conversation (from speech recognition, so ignore punctuation and "
            "capital letters). Reply with JSON only: {\"grammar\": 0-100 score for the learner's grammar, "
            "\"best\": the learner's best sentence (copy it), \"takeaway\": one short encouraging sentence on the most "
            "useful thing to improve, \"takeaway_bn\": the same in Bangla, \"better\": up to 3 items "
            "[{\"you\": a learner sentence copied exactly, \"better\": a more natural or correct version, \"tip\": a short "
            "reason in English, \"tip_bn\": the reason in Bangla, \"alts\": [3 other natural ways to say it]}]}. "
            "Choose sentences that can really be improved; if everything is correct, suggest more natural or advanced ways.",
            [{"role": "user", "content": convo}], max_tokens=1100))
        if data:
            _count_ai(learner, s, "report")
            g = data.get("grammar")
            report.update({
                "ai": True, "grammar": max(0, min(100, int(g))) if isinstance(g, (int, float)) else None,
                "best": str(data.get("best") or best)[:300], "takeaway": str(data.get("takeaway") or "")[:300],
                "takeaway_bn": str(data.get("takeaway_bn") or "")[:300],
                "better": [{"you": str(b.get("you", ""))[:300], "better": str(b.get("better", ""))[:300],
                            "tip": str(b.get("tip", ""))[:200], "tip_bn": str(b.get("tip_bn", ""))[:200],
                            "alts": [str(x)[:200] for x in (b.get("alts") or [])][:3]}
                           for b in (data.get("better") or []) if isinstance(b, dict) and b.get("better")][:3]})
    if not report["takeaway"]:
        if not turns:
            report["takeaway"] = "Say a few sentences next time so we can give you a report."
            report["takeaway_bn"] = "পরের বার কয়েকটি বাক্য বলুন, তাহলে রিপোর্ট দিতে পারব।"
        elif per_turn < 6:
            report["takeaway"] = "Try longer answers: add a reason with 'because' and an example."
            report["takeaway_bn"] = "আরও লম্বা উত্তর দিন: 'because' দিয়ে কারণ আর একটি উদাহরণ যোগ করুন।"
        else:
            report["takeaway"] = "Great length! Next time, try to use two of your new words again."
            report["takeaway_bn"] = "চমৎকার! পরের বার নতুন শব্দগুলোর দুটি আবার ব্যবহার করুন।"
    scores = [x for x in (report["pronunciation"], report["fluency"], report["grammar"]) if x is not None]
    report["score"] = round(sum(scores) / len(scores)) if scores else 0
    s.report = report
    s.finished_at = timezone.now()
    s.save(update_fields=["report", "finished_at"])
    if turns:
        _, first = E.finish(learner, f"talk:{s.pk}", s.title, report["score"])
        report["first"] = first
    return report


def practice_score(target, said, confidence=None):
    return {"score": E.speech_score(target, said, confidence), "marks": E.word_marks(target, said)}


# ------------------------------------------------------------------ JSON shapes shared by web and app

def session_json(s):
    return {"id": s.pk, "kind": s.kind, "title": s.title, "setting": s.setting, "persona": s.persona, "goal": s.goal,
            "messages": s.messages, "finished": bool(s.report), "max_turns": MAX_TURNS}


def profile_json(p):
    return {"level": p.level, "reason": p.reason, "challenge": p.challenge, "correct": p.correct, "interests": p.interests,
            "voice": p.voice, "speed": p.speed, "daily_minutes": p.daily_minutes, "done": p.done}


def save_profile(p, data):
    """Update a TalkProfile from a dict (web form or app JSON); unknown values are ignored."""
    def pick(key, allowed, cast=str):
        v = data.get(key)
        try:
            v = cast(v)
        except (TypeError, ValueError):
            return
        if v in allowed:
            setattr(p, key, v)
    pick("level", {n for n, *_ in T.LEVELS}, int)
    pick("reason", {k for k, *_ in T.REASONS})
    pick("challenge", {k for k, *_ in T.CHALLENGES})
    pick("correct", {k for k, *_ in T.CORRECT})
    pick("voice", {k for k, *_ in T.VOICES})
    pick("speed", {v for v, _ in T.SPEEDS}, float)
    pick("daily_minutes", set(T.DAILY_GOALS), int)
    interests = data.get("interests")
    if isinstance(interests, (list, tuple)):
        p.interests = [k for k in interests if k in T.BY_KEY][:18]
    p.done = True
    p.save()
    return p
