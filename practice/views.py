import json
import random
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.db.models import Avg, Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.models import Learner
from core.access import paid_required
from core.utils import family_required, learner_required
from learning import stats
from learning.models import Placement, PlacementQuestion, PracticeItem
from learning.placement import READER_MAX, READER_MIN, score_ladder, score_young_child

from growth.engine import award, xp_today

from . import ai, feedback
from .models import (LEARNED_BOX, CardReview, SkillCheck, SpeakingAttempt, SupportTicket,
                     TutorMessage, Tutorial, VocabDeck, VocabWord, WritingAttempt)
from .seed_data import SPEAKING, TYPING_TEXTS, WRITING_PROMPTS

DAILY_CAPS = {"flashcards": 30, "dictation": 30, "speaking": 20, "writing": 25, "typing": 20}


def _award_capped(learner, amount, reason):
    """Small XP for practice tools, with a daily cap so XP stays fair."""
    left = DAILY_CAPS.get(reason, 20) - xp_today(learner, reason)
    if left > 0:
        award(learner, min(amount, left), reason)

CHECK_SKILLS = [
    ("phonics", "Phonics", "🔤", "Letter sounds and blending — for little learners (Levels 0–2)."),
    ("listening", "Listening", "👂", "Listen to sentences and choose the answer (Levels 3–8)."),
    ("reading", "Reading", "📖", "Read short texts and answer (Levels 3–8)."),
    ("writing", "Writing", "✍️", "Choose the right word for grammar (Levels 3–8)."),
]
SKILL_NAMES = {k: name for k, name, _, _ in CHECK_SKILLS}
SKILL_NAMES["speaking"] = "Speaking"


def _current_level(learner, skill=None):
    p = learner.placements.first()
    if not p:
        return 0
    if skill and skill in p.skill_levels():
        return p.skill_levels()[skill]
    return p.overall


def _shuffle(choices):
    return random.sample(choices, len(choices))


# ------------------------------------------------------------------ level checks & practice

@paid_required("Skill checks", "দক্ষতা যাচাই")
def checks(request):
    learner = request.learner
    latest = {}
    for c in learner.skill_checks.all()[:60]:
        latest.setdefault((c.kind, c.skill), c)
    cards = []
    for key, name, emoji, desc in CHECK_SKILLS:
        cards.append({"key": key, "name": name, "emoji": emoji, "desc": desc,
                      "check": latest.get(("level_check", key)),
                      "practice": latest.get(("practice", key))})
    return render(request, "practice/checks.html", {
        "cards": cards, "placement": learner.placements.first(),
        "dictation": latest.get(("dictation", "dictation")),
    })


@paid_required("Skill checks", "দক্ষতা যাচাই", free_if=lambda r, skill: skill == "phonics")
def level_check(request, skill):
    if skill not in SKILL_NAMES or skill == "speaking":
        return redirect("practice:checks")
    learner = request.learner
    if skill == "phonics":
        qs = PlacementQuestion.objects.filter(skill="phonics", level__lte=2)
    else:
        qs = PlacementQuestion.objects.filter(skill=skill, level__gte=READER_MIN, level__lte=READER_MAX)
    questions = list(qs.order_by("level", "id"))

    if request.method == "POST":
        right = sum(1 for q in questions
                    if request.POST.get(str(q.id), "").strip().lower() == q.answer.strip().lower())
        if skill == "phonics":
            level = score_young_child(request.POST)
        else:
            by_level = {}
            for q in questions:
                ok = request.POST.get(str(q.id), "").strip().lower() == q.answer.strip().lower()
                by_level[q.level] = by_level.get(q.level, True) and ok
            level = score_ladder(by_level, READER_MIN, READER_MAX)
        check = SkillCheck.objects.create(learner=learner, kind=SkillCheck.Kind.LEVEL_CHECK, skill=skill,
                                          level=level, score=right, total=len(questions))
        # Update the learner's levels: phonics sets all four skills, others just their own.
        prev = learner.placements.first()
        levels = prev.skill_levels() if prev else {"listening": level, "speaking": level,
                                                   "reading": level, "writing": level}
        if skill == "phonics":
            levels = {k: level for k in levels}
        else:
            levels[skill] = level
        Placement.objects.create(learner=learner, young_child_test=(skill == "phonics"),
                                 overall=round(sum(levels.values()) / 4), **levels)
        return redirect("practice:check_result", pk=check.pk)

    for q in questions:
        q.shuffled = _shuffle(q.choice_list())
    return render(request, "practice/level_check.html", {
        "skill": skill, "name": SKILL_NAMES[skill], "questions": questions,
        "young": skill == "phonics",
    })


@paid_required("Skill checks", "দক্ষতা যাচাই", free_if=lambda r, pk: r.learner.skill_checks.filter(pk=pk, skill="phonics").exists())
def check_result(request, pk):
    check = get_object_or_404(SkillCheck, pk=pk, learner=request.learner)
    history = request.learner.skill_checks.filter(kind=check.kind, skill=check.skill)[:8]
    return render(request, "practice/check_result.html", {
        "check": check, "name": SKILL_NAMES.get(check.skill, check.skill.title()),
        "history": list(reversed(list(history))),
    })


def _practice_items(learner, skill):
    """Quiz questions from lessons of this skill, up to one level above the learner."""
    top = min(_current_level(learner, skill) + 1, 8)
    base = PracticeItem.objects.exclude(choices="").select_related("lesson__module__level")
    if skill == "phonics":
        qs = base.filter(lesson__skill="phonics")
    else:
        qs = base.filter(lesson__skill=skill, lesson__module__level__number__lte=top)
        if qs.count() < 5:  # thin skill: widen to all quiz questions at this learner's levels
            qs = base.filter(lesson__module__level__number__lte=max(top, 3),
                             lesson__module__level__number__gte=3)
    items = list(qs)
    random.shuffle(items)
    return items[:10]


@paid_required("Skill practice", "দক্ষতা অনুশীলন", free_if=lambda r, skill: skill == "phonics")
def skill_practice(request, skill):
    if skill not in SKILL_NAMES or skill == "speaking":
        return redirect("practice:checks")
    learner = request.learner
    if request.method == "POST":
        ids = [int(i) for i in request.POST.getlist("item") if i.isdigit()]
        items = {it.id: it for it in PracticeItem.objects.filter(id__in=ids)}
        results = []
        for i in ids:
            it = items.get(i)
            if not it:
                continue
            given = request.POST.get(f"a{i}", "")
            results.append({"item": it, "given": given,
                            "ok": given.strip().lower() == it.answer.strip().lower()})
        right = sum(r["ok"] for r in results)
        SkillCheck.objects.create(learner=learner, kind=SkillCheck.Kind.PRACTICE, skill=skill,
                                  score=right, total=len(results))
        return render(request, "practice/practice_result.html", {
            "skill": skill, "name": SKILL_NAMES[skill], "results": results, "right": right,
            "total": len(results)})
    items = _practice_items(learner, skill)
    for it in items:
        it.shuffled = _shuffle(it.choice_list())
    return render(request, "practice/skill_practice.html", {
        "skill": skill, "name": SKILL_NAMES[skill], "items": items})


# ------------------------------------------------------------------ word dictation

def _dictation_words(level_name):
    if level_name == "easy":
        words = [(it.prompt, it.picture, it.meaning_bn) for it in
                 PracticeItem.objects.filter(lesson__module__level__number=0)]
    elif level_name == "medium":
        words = [(it.prompt, it.picture, it.meaning_bn) for it in
                 PracticeItem.objects.filter(lesson__activity="dictation",
                                             lesson__module__level__number__in=[1, 2])]
        words += [(w.word, w.emoji, w.meaning_bn) for w in VocabWord.objects.filter(deck__level__lte=3)]
    elif level_name == "hard":
        words = [(w.word, w.emoji, w.meaning_bn) for w in VocabWord.objects.filter(deck__level__gte=3)
                 if " " not in w.word and len(w.word) >= 5]
    else:  # mixed: some of each level
        parts = [_dictation_words(x) for x in ("easy", "medium", "hard")]
        for part in parts:
            random.shuffle(part)
        mixed = parts[0][:7] + parts[1][:7] + parts[2][:7]
        return mixed
    seen, out = set(), []
    for w in words:
        if w[0].isalpha() and w[0].lower() not in seen:
            seen.add(w[0].lower())
            out.append({"word": w[0].lower(), "emoji": w[1], "bn": w[2]})
    return out


@paid_required("Dictation", "শ্রুতিলিখন")
def dictation(request):
    level_name = request.GET.get("level", "easy")
    if level_name not in ("easy", "medium", "hard", "mixed"):
        level_name = "easy"
    mode = "test" if request.GET.get("mode") == "test" else "practice"
    pool = _dictation_words(level_name)
    random.shuffle(pool)
    words = pool[:20 if mode == "test" else 10]
    started = "level" in request.GET
    return render(request, "practice/dictation.html", {
        "level_name": level_name, "mode": mode, "words": words, "started": started,
        "best": request.learner.skill_checks.filter(kind="dictation").order_by("-score").first(),
    })


@require_POST
@paid_required("Dictation", "শ্রুতিলিখন")
def dictation_save(request):
    try:
        score = int(request.POST.get("score", 0))
        total = int(request.POST.get("total", 0))
    except ValueError:
        return redirect("practice:dictation")
    total = max(0, min(total, 20))
    score = max(0, min(score, total))
    detail = f"{request.POST.get('level', 'easy')} · {request.POST.get('mode', 'practice')}"[:40]
    SkillCheck.objects.create(learner=request.learner, kind=SkillCheck.Kind.DICTATION,
                              skill="dictation", score=score, total=total, detail=detail)
    _award_capped(request.learner, score, "dictation")
    messages.success(request, f"Saved: {score} of {total} words right.")
    return redirect("practice:dictation")


# ------------------------------------------------------------------ speaking practice

@paid_required("Speaking practice with feedback", "ফিডব্যাকসহ কথা বলার অনুশীলন")
def speaking(request):
    learner = request.learner
    level = _current_level(learner, "speaking")
    try:
        level = int(request.GET.get("level", level))
    except ValueError:
        pass
    level = max(0, min(level, 8))
    mode, prompts = SPEAKING[level]
    recent = learner.speaking_attempts.all()[:6]
    return render(request, "practice/speaking.html", {
        "level": level, "mode": mode, "prompts": prompts, "recent": recent,
        "levels": range(9), "ai_on": ai.enabled(), "ai_left": ai.left_today(learner),
    })


@require_POST
@paid_required("Speaking practice with feedback", "ফিডব্যাকসহ কথা বলার অনুশীলন")
def speaking_save(request):
    learner = request.learner
    try:
        data = json.loads(request.body.decode() or "{}")
    except ValueError:
        return JsonResponse({"error": "bad request"}, status=400)
    target = (data.get("target") or "")[:300]
    heard = (data.get("heard") or "")[:1000]
    mode = "answer" if data.get("mode") == "answer" else "repeat"
    fb, used_ai = "", False
    if mode == "repeat":
        score = feedback.speaking_score(target, heard)
        missed = feedback.missed_words(target, heard)
    else:
        n = len(heard.split())
        score = min(100, n * 5)  # 20+ words = 100: rewards speaking at length
        missed = []
        if heard and ai.left_today(learner) > 0:
            fb = ai.ask(
                "The learner answered a speaking question out loud; this is the speech-to-text "
                "transcript, so ignore punctuation and small recognition errors. Give 2-3 short tips: "
                "one thing done well, one grammar or word fix with the better sentence, and one idea "
                "to say more. End with one line in Bangla. Under 90 words.",
                [{"role": "user", "content": f"Question: {target}\nAnswer: {heard}"}], max_tokens=300) or ""
            used_ai = bool(fb)
        if not fb:
            fb = ("Good! Try to give a reason with 'because' and an example." if n >= 12 else
                  "Try to say more: answer, then a reason ('because …'), then an example.")
    attempt = SpeakingAttempt.objects.create(learner=learner, target=target, heard=heard,
                                             score=score, mode=mode, feedback=fb, ai_used=used_ai)
    if heard:
        _award_capped(learner, 3, "speaking")
    return JsonResponse({"score": attempt.score, "missed": missed, "feedback": fb})


# ------------------------------------------------------------------ writing helper

def _prompt_band(level):
    return "young" if level <= 3 else "mid" if level <= 5 else "high"


MODEL_FRAME_BN = ("AI চালু থাকলে এখানে আপনার লেভেলের একটি মডেল উত্তর আসবে। এখন এই কাঠামোতে লিখুন:\n"
                  "1) মূল বাক্য: প্রশ্নের সরাসরি উত্তর।\n2) কারণ: because …\n3) উদাহরণ: For example, …\n"
                  "4) শেষ বাক্য: So / That is why …")


def _model_answer(learner, prompt, level):
    reply = None
    if prompt and ai.left_today(learner) > 0:
        reply = ai.ask(
            "Write a model answer to the writing task for an English learner at level "
            f"{level} of 0-8 (0 = beginner, 8 = advanced). Use language just a little above that level, "
            "clear paragraphs and useful linking words. Then add one line starting 'Useful phrases:' "
            "listing 3-4 phrases from the answer. Under 160 words in total.",
            [{"role": "user", "content": prompt}], max_tokens=500)
    return reply


@paid_required("Writing practice with marking", "মূল্যায়নসহ লেখার অনুশীলন")
def writing(request):
    from course.models import band_of_level
    from course.smart_test import rule_writing_level

    learner = request.learner
    level = _current_level(learner, "writing")
    prompts = WRITING_PROMPTS[_prompt_band(level)]
    result, model, estimate = None, None, None
    if request.method == "POST" and request.POST.get("action") == "model":
        prompt = (request.POST.get("prompt") or "").strip()[:300]
        if not prompt:
            messages.error(request, "Choose or type a topic first, then ask for a model answer.")
            return redirect("practice:writing")
        model = {"prompt": prompt, "text": _model_answer(learner, prompt, level)}
        if model["text"]:
            WritingAttempt.objects.create(learner=learner, prompt=prompt[:200], text="(model answer)",
                                          corrected=model["text"], ai_used=True)
        else:
            model["text"] = MODEL_FRAME_BN
    elif request.method == "POST":
        text = (request.POST.get("text") or "").strip()[:2000]
        prompt = (request.POST.get("prompt") or "")[:200]
        if not text:
            messages.error(request, "Please write something first.")
            return redirect("practice:writing")
        corrected, notes = feedback.check_writing(text)
        used_ai = False
        ai_level = None
        if ai.left_today(learner) > 0:
            reply = ai.ask(
                "Correct the learner's English writing. Reply ONLY with JSON: "
                '{"corrected": "<the full corrected text>", "notes": ["<short note>", ...], "level": 0-8}. '
                "Keep the learner's meaning and level; fix grammar, spelling and punctuation. "
                "Each note explains one fix in Bangla, with the English words in English. Max 5 notes. "
                "level = the writing level on a 0-8 scale (3 simple sentences, 5 good paragraph with some "
                "errors, 7 wide range and accurate)." + (f" The task was: {prompt}" if prompt else ""),
                [{"role": "user", "content": text}], max_tokens=800)
            if reply:
                try:
                    start, end = reply.find("{"), reply.rfind("}")
                    parsed = json.loads(reply[start:end + 1])
                    corrected = parsed.get("corrected") or corrected
                    notes = [str(n) for n in parsed.get("notes", [])][:6] or notes
                    if isinstance(parsed.get("level"), (int, float)):
                        ai_level = max(0, min(8, int(parsed["level"])))
                    used_ai = True
                except (ValueError, AttributeError):
                    pass
        lv = ai_level if ai_level is not None else rule_writing_level(text, 40)[0]
        estimate = {"level": lv, "band": band_of_level(lv).label, "ai": ai_level is not None}
        result = WritingAttempt.objects.create(learner=learner, prompt=prompt, text=text,
                                               corrected=corrected, feedback="\n".join(notes),
                                               ai_used=used_ai)
        _award_capped(learner, 5, "writing")
    return render(request, "practice/writing.html", {
        "prompts": prompts, "result": result, "model": model, "estimate": estimate,
        "history": learner.writing_attempts.exclude(text="(model answer)")[:5],
        "ai_on": ai.enabled(), "ai_left": ai.left_today(learner),
    })


# ------------------------------------------------------------------ AI tutor

TUTOR_SYSTEM = (
    "You are 'Tuntuni', the friendly FamilyEnglish tutor bird. Answer English-learning questions: "
    "sounds, words, grammar, speaking tips, and how to use FamilyEnglish (lessons, study plan, "
    "level checks, flashcards, family plan). Keep answers under 120 words, with one example. "
    "Learner: {name}, {role}, about level {level} of 0-8 (0 = letter sounds, 8 = advanced)."
)


@paid_required("Tuntuni, the English helper", "টুনটুনি, ইংরেজি সহায়ক")
def tutor(request):
    learner = request.learner
    if request.method == "POST":
        text = (request.POST.get("message") or "").strip()[:600]
        if text:
            TutorMessage.objects.create(learner=learner, role="user", text=text)
            answer, used = None, False
            if ai.left_today(learner) > 0:
                history = list(learner.tutor_messages.order_by("-created_at", "-id")[:10])[::-1]
                msgs = [{"role": m.role, "content": m.text} for m in history]
                answer = ai.ask(TUTOR_SYSTEM.format(name=learner.name, role=learner.get_role_display(),
                                                    level=_current_level(learner)), msgs)
                used = bool(answer)
            if not answer:
                answer = feedback.faq_answer(text)
            TutorMessage.objects.create(learner=learner, role="assistant", text=answer, ai_used=used)
        return redirect("practice:tutor")
    day = request.GET.get("day")
    all_msgs = learner.tutor_messages.all()
    if day:
        msgs = list(all_msgs.filter(created_at__date=day)[:200])
    else:
        msgs = list(learner.tutor_messages.order_by("-created_at", "-id")[:40])[::-1]
    days = list(all_msgs.dates("created_at", "day", order="DESC")[:14])
    return render(request, "practice/tutor.html", {
        "chat": msgs, "ai_on": ai.enabled(), "ai_left": ai.left_today(learner), "days": days, "day": day,
        "greeting": _tutor_greeting(learner),
        "suggestions": _tutor_suggestions(learner),
    })


def _tutor_greeting(learner):
    """A personal hello: level, today's task, due cards and the weakest question type."""
    from course.models import AnswerLog
    from course.qtypes import label
    from learning import planner

    p = learner.placements.first()
    _, mission = planner.today_mission(learner, timezone.localdate())
    due = CardReview.objects.filter(learner=learner, due__lte=timezone.localdate()).count()
    since = timezone.now() - timedelta(days=30)
    weak = (AnswerLog.objects.filter(learner=learner, correct=False, created_at__gte=since).exclude(qtype="")
            .values("qtype").annotate(n=Count("id")).order_by("-n").first())
    return {"name": learner.name, "level": p.overall if p else None,
            "task": mission.title if mission else None, "due": due,
            "weak": label(weak["qtype"]) if weak else None}


def _tutor_suggestions(learner):
    g = _tutor_greeting(learner)
    out = []
    if g["weak"]:
        out.append(f"Help me with {g['weak'].lower()}")
    if g["task"]:
        out.append(f"Explain today's lesson: {g['task']}")
    out += ["How do I say “th”?", "When do I use “an”?", "Give me 3 new words for today",
            "আমার প্ল্যান কীভাবে বদলাবো?"]
    return out[:6]


@family_required
def tutor_history(request, learner_pk):
    """Parents can read a learner's tutor chat."""
    learner = get_object_or_404(Learner, pk=learner_pk, family=request.family)
    return render(request, "practice/tutor_history.html", {
        "learner": learner, "chat": learner.tutor_messages.all()[:200]})


# ------------------------------------------------------------------ vocabulary

@paid_required("Flashcards", "ফ্ল্যাশকার্ড")
def vocab(request):
    learner = request.learner
    today = timezone.localdate()
    reviews = CardReview.objects.filter(learner=learner)
    by_deck = {}
    for r in reviews.select_related("word"):
        d = by_deck.setdefault(r.word.deck_id, {"seen": 0, "learned": 0, "due": 0})
        d["seen"] += 1
        d["learned"] += r.box >= LEARNED_BOX
        d["due"] += r.due <= today
    band = request.GET.get("band", "")
    q = (request.GET.get("q") or "").strip()[:40]
    decks = VocabDeck.objects.filter(series="").annotate(n=Count("words"))
    found = []
    if q:
        found = list(VocabWord.objects.filter(word__icontains=q).select_related("deck")[:20]) + \
            list(VocabWord.objects.filter(meaning_bn__icontains=q).select_related("deck")[:10])
        decks = decks.filter(Q(title__icontains=q) | Q(title_bn__icontains=q) | Q(words__word__icontains=q)).distinct()
    bands = ["Beginner", "Elementary", "Intermediate", "Advanced"]
    rows = []
    for deck in decks:
        if band and deck.band != band:
            continue
        s = by_deck.get(deck.id, {"seen": 0, "learned": 0, "due": 0})
        rows.append({"deck": deck, **s, "percent": round(s["learned"] * 100 / deck.n) if deck.n else 0})
    return render(request, "practice/vocab.html", {
        "rows": rows, "bands": bands, "band": band,
        "total_learned": reviews.filter(box__gte=LEARNED_BOX).count(),
        "total_due": reviews.filter(due__lte=today).count(),
        "total_seen": reviews.count(),
        "deck_count": VocabDeck.objects.filter(series="").count(),
        "missed": reviews.filter(last_grade=CardReview.FORGOT, times_seen__gt=0).count(),
        "q": q, "found": found,
    })


@paid_required("Flashcards", "ফ্ল্যাশকার্ড")
def vocab_study(request, slug=None):
    """Due cards first, then up to 10 new cards. slug=None studies due cards from every deck.

    ?mode=missed studies the words marked 'Forgot'; ?view=list shows the deck as a table."""
    learner = request.learner
    today = timezone.localdate()
    deck = get_object_or_404(VocabDeck, slug=slug) if slug else None
    mode = request.GET.get("mode", "")
    words = VocabWord.objects.select_related("deck")
    if deck:
        words = words.filter(deck=deck)
    reviewed = CardReview.objects.filter(learner=learner)
    if request.GET.get("view") == "list" and deck:
        boxes = {r.word_id: r for r in reviewed.filter(word__deck=deck)}
        rows = [{"w": w, "r": boxes.get(w.id)} for w in words]
        return render(request, "practice/vocab_list.html", {"deck": deck, "rows": rows,
                                                            "learned_box": LEARNED_BOX})
    if mode == "missed":
        cards = list(words.filter(id__in=reviewed.filter(last_grade=CardReview.FORGOT, times_seen__gt=0)
                                  .values_list("word_id", flat=True)))
    else:
        due_ids = list(reviewed.filter(due__lte=today, word__in=words).values_list("word_id", flat=True))
        seen_ids = set(reviewed.values_list("word_id", flat=True))
        cards = list(words.filter(id__in=due_ids))
        if deck:
            cards += [w for w in words if w.id not in seen_ids][:10]
    random.shuffle(cards)
    return render(request, "practice/vocab_study.html", {
        "deck": deck, "mode": mode,
        "cards": [{"id": w.id, "word": w.word, "emoji": w.emoji, "bn": w.meaning_bn, "example": w.example,
                   "pos": w.pos, "definition": w.definition, "ipa": w.ipa} for w in cards[:20]],
    })


@require_POST
@paid_required("Flashcards", "ফ্ল্যাশকার্ড")
def vocab_rate(request):
    try:
        data = json.loads(request.body.decode() or "{}")
        word = VocabWord.objects.get(pk=int(data.get("word")))
    except (ValueError, TypeError, VocabWord.DoesNotExist):
        return JsonResponse({"error": "bad request"}, status=400)
    if "grade" in data:
        try:
            grade = max(0, min(2, int(data["grade"])))
        except (TypeError, ValueError):
            return JsonResponse({"error": "bad request"}, status=400)
    else:
        grade = CardReview.KNEW if data.get("knew") else CardReview.FORGOT
    review, _ = CardReview.objects.get_or_create(learner=request.learner, word=word)
    review.rate(grade)
    _award_capped(request.learner, 1 + (grade == CardReview.KNEW), "flashcards")
    return JsonResponse({"box": review.box, "due": review.due.isoformat()})


# ------------------------------------------------------------------ reports & streaks

def _best_streak(learner):
    days = sorted({timezone.localtime(p.completed_at).date() for p in learner.progress.all()})
    best = run = 0
    prev = None
    for d in days:
        run = run + 1 if prev and d - prev == timedelta(days=1) else 1
        best = max(best, run)
        prev = d
    return best


@paid_required("Parent reports", "অভিভাবক রিপোর্ট")
def reports(request):
    learner = request.learner
    placements = list(learner.placements.order_by("taken_at")[:12])
    checks = learner.skill_checks.all()[:20]
    speak = learner.speaking_attempts.aggregate(avg=Avg("score"), n=Count("id"))
    reviews = CardReview.objects.filter(learner=learner)
    st = stats.learner_stats(learner)
    skills = ["listening", "speaking", "reading", "writing"]
    level_rows = []
    latest = placements[-1] if placements else None
    first = placements[0] if placements else None
    for s in skills:
        level_rows.append({"skill": s.title(), "now": getattr(latest, s, None),
                           "start": getattr(first, s, None),
                           "percent": round((getattr(latest, s, 0) or 0) * 100 / 8)})
    return render(request, "practice/reports.html", {
        "placements": placements, "checks": checks, "level_rows": level_rows,
        "speak_avg": round(speak["avg"] or 0), "speak_n": speak["n"],
        "writing_n": learner.writing_attempts.count(),
        "words_learned": reviews.filter(box__gte=LEARNED_BOX).count(),
        "words_seen": reviews.count(),
        "stats": st, "best_streak": max(_best_streak(learner), st["streak"]),
        "activity": stats.activity(learner, 84),
        "board": stats.leaderboard(request.family),
        "skill_progress": stats.skill_progress(learner),
        **_course_reports(learner),
    })


def _course_reports(learner):
    """Self-test and AI-test summary for My Reports (completed, scored, best, this week)."""
    from course.models import COURSE_SKILLS, SKILL_EMOJI, CourseProgress, SelfTestAttempt

    week = timezone.now() - timedelta(days=7)
    attempts = SelfTestAttempt.objects.filter(learner=learner)
    rows = []
    for skill in COURSE_SKILLS:
        a = attempts.filter(lesson__skill=skill)
        agg = a.aggregate(avg=Avg("percent"), n=Count("id"))
        rows.append({"skill": skill, "emoji": SKILL_EMOJI[skill], "n": agg["n"], "avg": round(agg["avg"] or 0),
                     "best": a.order_by("-percent").values_list("percent", flat=True).first(),
                     "passed": CourseProgress.objects.filter(learner=learner, passed=True, lesson__skill=skill).count(),
                     "week": a.filter(created_at__gte=week).count()})
    return {"course_rows": rows, "selftests": attempts.select_related("lesson")[:15],
            "smart_tests": learner.smart_tests.filter(finished_at__isnull=False)[:5],
            "course_totals": {"tests": attempts.count(), "passed": attempts.filter(passed=True).count(),
                              "week": attempts.filter(created_at__gte=week).count(),
                              "best": attempts.order_by("-percent").values_list("percent", flat=True).first()}}


# ------------------------------------------------------------------ refer & earn

def _mask(name):
    words = (name or "Family").split()
    return " ".join(w[0] + "•" * max(1, min(4, len(w) - 1)) for w in words)


@family_required
def refer(request):
    from core.models import Family, PayoutRequest, ReferralEarning

    fam = request.family
    if not fam.referral_code:
        fam.save()  # generates a code for families created before referrals existed
    today = timezone.localdate()
    earnings = ReferralEarning.objects.filter(family=fam)
    free = earnings.filter(payout__isnull=True)
    available = free.filter(available_on__lte=today).aggregate(s=Sum("amount_bdt"))["s"] or 0
    on_hold = free.filter(available_on__gt=today).aggregate(s=Sum("amount_bdt"))["s"] or 0
    paid = (earnings.filter(payout__status=PayoutRequest.Status.PAID).aggregate(s=Sum("amount_bdt"))["s"] or 0)
    if request.method == "POST":
        number = "".join(ch for ch in request.POST.get("bkash", "") if ch.isdigit())
        if available < settings.REFERRAL_MIN_PAYOUT:
            messages.error(request, f"You can withdraw from ৳{settings.REFERRAL_MIN_PAYOUT}.")
        elif not (len(number) == 11 and number.startswith("01")):
            messages.error(request, "Please enter an 11-digit bKash number starting with 01.")
        elif fam.payouts.filter(status=PayoutRequest.Status.REQUESTED).exists():
            messages.info(request, "You already have a withdrawal request waiting.")
        else:
            payout = PayoutRequest.objects.create(family=fam, amount_bdt=available, bkash_number=number)
            free.filter(available_on__lte=today).update(payout=payout)
            messages.success(request, f"Withdrawal of ৳{available} requested. We usually pay within 3 working days.")
        return redirect("practice:refer")
    link = request.build_absolute_uri(reverse("core:signup") + f"?ref={fam.referral_code}")
    invited = fam.referrals.all().order_by("-created_at")
    top = (Family.objects.annotate(n=Count("referrals", filter=Q(referrals__referral_rewarded=True)))
           .filter(n__gt=0).order_by("-n")[:5])
    return render(request, "practice/refer.html", {
        "family": fam, "link": link, "invited": invited,
        "joined": invited.count(), "rewarded": invited.filter(referral_rewarded=True).count(),
        "reward_days": settings.REFERRAL_REWARD_DAYS, "extra_days": settings.REFERRAL_EXTRA_TRIAL_DAYS,
        "commission": settings.REFERRAL_COMMISSION_PCT, "hold_days": settings.REFERRAL_HOLD_DAYS,
        "min_payout": settings.REFERRAL_MIN_PAYOUT, "available": available, "on_hold": on_hold, "paid": paid,
        "payouts": fam.payouts.all()[:10], "earnings": earnings.select_related("from_family")[:10],
        "top": [{"name": _mask(f.name), "n": f.n, "me": f.id == fam.id} for f in top],
        "share_text": (f"আমরা FamilyEnglish-এ পরিবারের সবাই মিলে ইংরেজি শিখছি। এই লিংকে যোগ দিলে "
                       f"{settings.FREE_TRIAL_DAYS + settings.REFERRAL_EXTRA_TRIAL_DAYS} দিন ফ্রি: {link}"),
    })


# ------------------------------------------------------------------ tutorials & support

def tutorials(request):
    items = list(Tutorial.objects.all())
    try:
        current = int(request.GET.get("n", items[0].order if items else 1))
    except ValueError:
        current = 1
    selected = next((t for t in items if t.order == current), items[0] if items else None)
    if selected and selected.link_name:
        try:
            selected.link = reverse(selected.link_name)
        except NoReverseMatch:
            selected.link = ""
    groups = {}
    for t in items:
        groups.setdefault(t.group, []).append(t)
    return render(request, "practice/tutorials.html", {"groups": groups, "selected": selected,
                                                       "count": len(items)})


ALLOWED_UPLOADS = {".png": b"\x89PNG", ".jpg": b"\xff\xd8", ".jpeg": b"\xff\xd8", ".webp": b"RIFF"}


def _valid_screenshot(f):
    import os
    ext = os.path.splitext(f.name)[1].lower()
    if ext not in ALLOWED_UPLOADS or f.size > settings.SUPPORT_MAX_UPLOAD_MB * 1024 * 1024:
        return False
    head = f.read(8)
    f.seek(0)
    return head.startswith(ALLOWED_UPLOADS[ext])


@family_required
def support(request):
    fam = request.family
    if request.method == "POST":
        subject = (request.POST.get("subject") or "").strip()[:120]
        message = (request.POST.get("message") or "").strip()[:3000]
        shot = request.FILES.get("attachment")
        if shot and not _valid_screenshot(shot):
            messages.error(request, f"Screenshots must be PNG, JPG or WEBP and under {settings.SUPPORT_MAX_UPLOAD_MB} MB.")
        elif subject and message:
            SupportTicket.objects.create(family=fam, user=request.user, subject=subject, message=message,
                                         attachment=shot or "")
            messages.success(request, "Thank you. We will reply here within 1–2 days.")
            return redirect("practice:support")
        else:
            messages.error(request, "Please write a subject and a message.")
    tab = request.GET.get("tab", "open")
    if tab not in SupportTicket.Status.values:
        tab = "open"
    tickets = fam.tickets.all()
    counts = {k: tickets.filter(status=k).count() for k in SupportTicket.Status.values}
    return render(request, "practice/support.html", {
        "tickets": tickets.filter(status=tab)[:30], "tab": tab, "counts": counts,
        "tabs": SupportTicket.Status.choices, "max_mb": settings.SUPPORT_MAX_UPLOAD_MB})


@family_required
def support_file(request, pk):
    """Screenshots are only shown to the family that sent them (and staff in the admin)."""
    from django.http import FileResponse, Http404

    t = get_object_or_404(SupportTicket, pk=pk)
    if not (t.family_id == request.family.id or request.user.is_staff) or not t.attachment:
        raise Http404
    return FileResponse(t.attachment.open("rb"))


# ------------------------------------------------------------------ typing speed

@paid_required("Typing practice", "টাইপিং অনুশীলন")
def typing(request):
    learner = request.learner
    level = request.GET.get("level", "easy")
    if level not in TYPING_TEXTS:
        level = "easy"
    try:
        seconds = int(request.GET.get("time", 60))
    except ValueError:
        seconds = 60
    seconds = seconds if seconds in (30, 60, 120) else 60
    tests = learner.skill_checks.filter(kind=SkillCheck.Kind.TYPING)
    trend = list(tests[:12])[::-1]
    leaders = []
    for l in request.family.learners.all():
        best = l.skill_checks.filter(kind=SkillCheck.Kind.TYPING).order_by("-score").first()
        if best:
            leaders.append({"learner": l, "wpm": best.score})
    leaders.sort(key=lambda r: -r["wpm"])
    return render(request, "practice/typing.html", {
        "level": level, "seconds": seconds, "text": " ".join(random.sample(TYPING_TEXTS[level], 3)),
        "best": tests.order_by("-score").first(), "trend": trend, "leaders": leaders,
        "levels": [("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")], "times": [30, 60, 120],
    })


@require_POST
@paid_required("Typing practice", "টাইপিং অনুশীলন")
def typing_save(request):
    try:
        wpm = max(0, min(200, int(request.POST.get("wpm", 0))))
        acc = max(0, min(100, int(request.POST.get("accuracy", 0))))
        secs = int(request.POST.get("seconds", 60))
    except ValueError:
        return redirect("practice:typing")
    level = request.POST.get("level", "easy")[:10]
    SkillCheck.objects.create(learner=request.learner, kind=SkillCheck.Kind.TYPING, skill="typing",
                              score=wpm, total=100, detail=f"{level} · {secs}s · {acc}%")
    _award_capped(request.learner, 5, "typing")
    messages.success(request, f"Saved: {wpm} words per minute, {acc}% accuracy.")
    return redirect(f"{reverse('practice:typing')}?level={level}&time={secs}")


# ------------------------------------------------------------------ dashboard helpers

def nav_counts(learner):
    """Small numbers for the sidebar (due flashcards)."""
    if not learner:
        return {}
    return {"due_cards": CardReview.objects.filter(learner=learner, due__lte=timezone.localdate()).count()}

