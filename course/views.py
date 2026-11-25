import json
import random
from datetime import timedelta

from django.contrib import messages
from django.db.models import Count, Q
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.access import paid_required
from core.utils import learner_required
from growth.engine import award
from learning import planner
from learning.models import PlanDay
from practice import ai

from . import grading, handouts, path, smart_test
from .models import (BAND_BN, BAND_ORDER, COURSE_SKILLS, PASS_PERCENT, SKILL_BN, SKILL_EMOJI, AnswerLog,
                     Band, CourseLesson, CourseProgress, CourseSkill, SelfTestAttempt, SmartTest)
from .qtypes import QTYPES, label as qtype_label


def _lang(request):
    return request.session.get("lang", "en")


def _level_hint(learner):
    p = learner.placements.first()
    return p.overall if p else None


def _cards(items, lesson=None, shuffle=True):
    """Items as the page shows them: no answers, choices shuffled, with question-type labels."""
    out = []
    for i, (it, src) in enumerate(items):
        card = grading.public_item(it)
        if shuffle and card.get("opts"):
            random.shuffle(card["opts"])
        card.update(i=src[1], slug=src[0], n=i + 1, qt_label=qtype_label(it.get("qt", "")))
        out.append(card)
    return out


def _progress_map(learner, lessons=None):
    qs = CourseProgress.objects.filter(learner=learner)
    if lessons is not None:
        qs = qs.filter(lesson__in=lessons)
    return {p.lesson_id: p for p in qs}


# ------------------------------------------------------------------ course home

@learner_required
def home(request):
    learner = request.learner
    test = learner.smart_tests.filter(finished_at__isnull=False).first()
    unfinished = learner.smart_tests.filter(finished_at__isnull=True).first()
    bands, levels, _ = path.start_bands(learner)
    progress = _progress_map(learner)
    grid = []
    for skill in COURSE_SKILLS:
        row = {"skill": skill, "name": CourseSkill(skill).label, "bn": SKILL_BN[skill],
               "emoji": SKILL_EMOJI[skill], "start": bands.get(skill, "easy"),
               "level": levels.get(skill), "bands": []}
        for band in BAND_ORDER:
            lessons = list(CourseLesson.objects.filter(skill=skill, band=band))
            passed = sum(1 for l in lessons if progress.get(l.id) and progress[l.id].passed)
            row["bands"].append({"band": band.value, "label": band.label, "bn": BAND_BN[band.value],
                                 "passed": passed, "total": len(lessons),
                                 "percent": round(passed * 100 / len(lessons)) if lessons else 0,
                                 "start": band.value == row["start"]})
        grid.append(row)
    next_up = path.build_path(learner, limit=6)
    for l in next_up:
        l.prog = progress.get(l.id)
    plan = learner.plans.filter(is_active=True).first()
    return render(request, "course/home.html", {
        "test": test, "unfinished": unfinished, "grid": grid, "next_up": next_up,
        "path_total": len(path.build_path(learner)), "plan": plan,
        "why": path.why_text(next_up[0], learner, _lang(request)) if next_up else "",
    })


@paid_required("The skill course (Listening, Speaking, Reading, Writing, Grammar)", "দক্ষতার কোর্স (শোনা, বলা, পড়া, লেখা, ব্যাকরণ)")
def skill_page(request, skill):
    if skill not in COURSE_SKILLS:
        raise Http404
    learner = request.learner
    bands, levels, _ = path.start_bands(learner)
    lessons = CourseLesson.objects.filter(skill=skill)
    progress = _progress_map(learner, lessons)
    columns = []
    for band in BAND_ORDER:
        rows = [l for l in lessons if l.band == band.value]
        for l in rows:
            l.prog = progress.get(l.id)
        columns.append({"band": band.value, "label": band.label, "bn": BAND_BN[band.value], "lessons": rows,
                        "start": bands.get(skill) == band.value})
    return render(request, "course/skill.html", {
        "skill": skill, "name": CourseSkill(skill).label, "bn": SKILL_BN[skill], "emoji": SKILL_EMOJI[skill],
        "columns": columns, "level": levels.get(skill), "skills": [(s, CourseSkill(s).label, SKILL_EMOJI[s])
                                                                   for s in COURSE_SKILLS],
    })


# ------------------------------------------------------------------ lesson, practice, self-test

def _neighbours(lesson):
    same = list(CourseLesson.objects.filter(skill=lesson.skill).order_by("band", "order"))
    same.sort(key=lambda l: (l.band_rank, l.order))
    i = same.index(lesson)
    return (same[i - 1] if i > 0 else None), (same[i + 1] if i + 1 < len(same) else None)


@paid_required("The skill course (Listening, Speaking, Reading, Writing, Grammar)", "দক্ষতার কোর্স (শোনা, বলা, পড়া, লেখা, ব্যাকরণ)")
def lesson(request, slug):
    lesson = get_object_or_404(CourseLesson, slug=slug)
    prog = CourseProgress.objects.filter(learner=request.learner, lesson=lesson).first()
    prev, nxt = _neighbours(lesson)
    cards = _cards([(it, (lesson.slug, i)) for i, it in enumerate(lesson.practice)])
    from learning.clips import clip_context
    return render(request, "course/lesson.html", {
        **clip_context(lesson),
        "lesson": lesson, "prog": prog, "cards": cards, "prev": prev, "next": nxt,
        "listening": lesson.skill == "listening", "ai_on": ai.enabled(),
        "ai_left": ai.left_today(request.learner), "pass_percent": PASS_PERCENT,
        "attempts": request.learner.selftests.filter(lesson=lesson)[:3],
        "why": path.why_text(lesson, request.learner, _lang(request)),
        "handouts": handouts.for_lesson(lesson.slug),
    })


@learner_required
def handbook(request):
    """The 23 printable pronunciation handbook lessons, with the app lesson for each."""
    titles = dict(CourseLesson.objects.values_list("slug", "title"))
    rows = [{**h, "links": [(s, titles[s]) for s in h["lessons"] if s in titles]} for h in handouts.items()]
    return render(request, "course/handbook.html", {"rows": rows, "full": request.family.has_full_access})


@paid_required("The pronunciation handbook PDFs", "উচ্চারণ হ্যান্ডবুকের PDF",
               free_if=lambda request, n: n in handouts.FREE, learner=False)
def handout(request, n):
    if n not in handouts.HANDOUTS or not handouts.path(n).exists():
        raise Http404
    return FileResponse(open(handouts.path(n), "rb"), content_type="application/pdf",
                        filename=f"FamilyEnglish-Lesson-{n:02d}.pdf")


@require_POST
@paid_required("The skill course (Listening, Speaking, Reading, Writing, Grammar)", "দক্ষতার কোর্স (শোনা, বলা, পড়া, লেখা, ব্যাকরণ)")
def check(request):
    """Mark one practice or drill answer and explain any mistake."""
    try:
        data = json.loads(request.body.decode() or "{}")
        lesson = CourseLesson.objects.get(slug=data.get("slug"))
        item = lesson.practice[int(data.get("i"))]
    except (ValueError, TypeError, IndexError, CourseLesson.DoesNotExist):
        return JsonResponse({"error": "bad request"}, status=400)
    learner = request.learner
    use_ai = item["t"] == "open" and ai.left_today(learner) > 0
    res = grading.check_item(item, data.get("answer", ""), use_ai=use_ai, level_hint=_level_hint(learner))
    source = "drill" if data.get("source") == "drill" else "practice"
    AnswerLog.objects.create(learner=learner, lesson=lesson, skill=lesson.skill, qtype=item.get("qt", ""),
                             source=source, correct=res["ok"], given=(data.get("answer") or "")[:300],
                             expected=(item.get("a") or "")[:300], ai_used=res["ai"])
    return JsonResponse(res)


@require_POST
@paid_required("The skill course (Listening, Speaking, Reading, Writing, Grammar)", "দক্ষতার কোর্স (শোনা, বলা, পড়া, লেখা, ব্যাকরণ)")
def practice_done(request, slug):
    lesson = get_object_or_404(CourseLesson, slug=slug)
    prog, _ = CourseProgress.objects.get_or_create(learner=request.learner, lesson=lesson)
    if not prog.practice_done:
        prog.practice_done = True
        prog.save()
    award(request.learner, 10, "practice", key=f"cpractice-{lesson.id}")
    return redirect("course:selftest", slug=slug)


def _stars(percent):
    return 3 if percent >= 90 else 2 if percent >= 75 else 1 if percent >= PASS_PERCENT else 0


@paid_required("The skill course (Listening, Speaking, Reading, Writing, Grammar)", "দক্ষতার কোর্স (শোনা, বলা, পড়া, লেখা, ব্যাকরণ)")
def selftest(request, slug):
    lesson = get_object_or_404(CourseLesson, slug=slug)
    learner = request.learner
    if request.method == "POST":
        review, right = [], 0
        for i, item in enumerate(lesson.selftest):
            given = request.POST.get(f"a{i}", "")
            res = grading.check_item(item, given)
            right += res["ok"]
            review.append({"q": item.get("q"), "say": item.get("say", ""), "t": item["t"], "given": given[:300],
                           "qt": qtype_label(item.get("qt", ""), _lang(request)), **res})
            AnswerLog.objects.create(learner=learner, lesson=lesson, skill=lesson.skill, qtype=item.get("qt", ""),
                                     source="selftest", correct=res["ok"], given=given[:300],
                                     expected=(item.get("a") or "")[:300])
        total = len(lesson.selftest)
        percent = round(right * 100 / total) if total else 0
        passed = percent >= PASS_PERCENT
        attempt = SelfTestAttempt.objects.create(learner=learner, lesson=lesson, score=right, total=total,
                                                 percent=percent, passed=passed, review=review)
        prog, _ = CourseProgress.objects.get_or_create(learner=learner, lesson=lesson)
        prog.attempts += 1
        if percent > prog.best_score:
            prog.best_score = percent
            prog.stars = max(prog.stars, _stars(percent))
        if passed and not prog.passed:
            prog.passed, prog.passed_at = True, timezone.now()
        prog.save()
        if passed:
            award(learner, 30, "self-test passed", key=f"course-{lesson.id}")
            for n in range(1, prog.stars + 1):
                award(learner, 10, "self-test stars", key=f"course-{lesson.id}-s{n}")
            from learning.planner import tick_days
            tick_days(learner, course_lesson=lesson)
        return redirect("course:result", pk=attempt.pk)
    items = []
    for i, it in enumerate(lesson.selftest):
        card = grading.public_item(it)
        if card.get("opts"):
            random.shuffle(card["opts"])
        card.update(i=i, n=i + 1, qt_label=qtype_label(it.get("qt", "")))
        items.append(card)
    return render(request, "course/selftest.html", {
        "lesson": lesson, "items": items, "listening": lesson.skill == "listening",
        "pass_percent": PASS_PERCENT,
    })


@paid_required("The skill course (Listening, Speaking, Reading, Writing, Grammar)", "দক্ষতার কোর্স (শোনা, বলা, পড়া, লেখা, ব্যাকরণ)")
def result(request, pk):
    attempt = get_object_or_404(SelfTestAttempt, pk=pk, learner=request.learner)
    lesson = attempt.lesson
    _, nxt = _neighbours(lesson)
    upcoming = path.build_path(request.learner, limit=1)
    return render(request, "course/result.html", {
        "attempt": attempt, "lesson": lesson, "next": nxt, "path_next": upcoming[0] if upcoming else None,
        "stars": _stars(attempt.percent), "mistakes": [r for r in attempt.review if not r["ok"]],
        "pass_percent": PASS_PERCENT,
    })


# ------------------------------------------------------------------ weak spots and drills

@paid_required("The skill course (Listening, Speaking, Reading, Writing, Grammar)", "দক্ষতার কোর্স (শোনা, বলা, পড়া, লেখা, ব্যাকরণ)")
def weak_spots(request):
    learner = request.learner
    since = timezone.now() - timedelta(days=90)
    rows = (AnswerLog.objects.filter(learner=learner, created_at__gte=since).exclude(qtype="")
            .values("qtype").annotate(n=Count("id"), wrong=Count("id", filter=Q(correct=False))))
    lang = _lang(request)
    spots = []
    for r in rows:
        if r["qtype"] not in QTYPES:
            continue
        acc = round((r["n"] - r["wrong"]) * 100 / r["n"]) if r["n"] else 0
        skill = QTYPES[r["qtype"]][0]
        spots.append({"qtype": r["qtype"], "label": qtype_label(r["qtype"], lang), "skill": skill,
                      "emoji": SKILL_EMOJI.get(skill, ""), "n": r["n"], "wrong": r["wrong"], "accuracy": acc})
    weak = sorted([s for s in spots if s["wrong"]], key=lambda s: (s["accuracy"], -s["wrong"]))[:5]
    recent = (AnswerLog.objects.filter(learner=learner, correct=False).exclude(expected="")
              .select_related("lesson")[:12])
    by_skill = {}
    for code, (skill, en, bn) in QTYPES.items():
        by_skill.setdefault(skill, []).append({"qtype": code, "label": bn if lang == "bn" else en,
                                               "stat": next((s for s in spots if s["qtype"] == code), None)})
    return render(request, "course/weak_spots.html", {
        "weak": weak, "recent": recent, "by_skill": [(s, SKILL_EMOJI[s], CourseSkill(s).label, by_skill.get(s, []))
                                                     for s in COURSE_SKILLS],
        "answered": sum(s["n"] for s in spots),
    })


@paid_required("The skill course (Listening, Speaking, Reading, Writing, Grammar)", "দক্ষতার কোর্স (শোনা, বলা, পড়া, লেখা, ব্যাকরণ)")
def drill(request, qtype):
    if qtype not in QTYPES:
        raise Http404
    learner = request.learner
    lessons = CourseLesson.objects.filter(skill=QTYPES[qtype][0])
    pool = [(it, (l.slug, i)) for l in lessons for i, it in enumerate(l.practice)
            if it.get("qt") == qtype and not (l.passage and l.skill == "listening")]
    random.shuffle(pool)
    cards = _cards(pool[:8])
    passages = {}
    for it, (slug, _) in pool[:8]:
        l = next(x for x in lessons if x.slug == slug)
        if l.passage and l.skill == "reading":
            passages[slug] = {"title": l.passage_title or l.title, "text": l.passage}
    for c in cards:
        c["passage"] = passages.get(c["slug"])
    return render(request, "course/drill.html", {
        "qtype": qtype, "label": qtype_label(qtype, _lang(request)), "cards": cards,
        "skill": QTYPES[qtype][0], "emoji": SKILL_EMOJI.get(QTYPES[qtype][0], ""),
    })


# ------------------------------------------------------------------ AI level test

@paid_required("The level test", "লেভেল টেস্ট")
def level_test(request):
    learner = request.learner
    tests = learner.smart_tests.filter(finished_at__isnull=False)[:5]
    unfinished = learner.smart_tests.filter(finished_at__isnull=True).first()
    return render(request, "course/level_test.html", {
        "tests": tests, "unfinished": unfinished, "ai_on": ai.enabled(),
        "young": learner.is_young_child,
    })


@require_POST
@paid_required("The level test", "লেভেল টেস্ট")
def level_test_start(request):
    learner = request.learner
    learner.smart_tests.filter(finished_at__isnull=True).delete()
    test = smart_test.start(learner)
    return redirect("course:level_step", pk=test.pk)


@paid_required("The level test", "লেভেল টেস্ট")
def level_step(request, pk):
    test = get_object_or_404(SmartTest, pk=pk, learner=request.learner)
    if test.done:
        return redirect("course:level_result", pk=test.pk)
    step = smart_test.current_step(test)
    if step is None:
        smart_test.finish(test)
        award(request.learner, 50, "AI level test", key=f"smart-{test.pk}")
        return redirect("course:level_result", pk=test.pk)
    skill, part = step.split(":")
    if request.method == "POST":
        if skill in smart_test.OBJECTIVE:
            smart_test.submit_objective(test, step, request.POST)
        elif skill == "writing":
            smart_test.submit_writing(test, request.POST.get("text", ""))
        elif skill == "speaking":
            smart_test.submit_speaking(test, [request.POST.get("r0", ""), request.POST.get("r1", "")],
                                       request.POST.get("open", ""), request.POST.get("typed") == "1")
        return redirect("course:level_step", pk=test.pk)

    ctx = {"test": test, "step": step, "skill": skill, "part": part,
           "number": test.step + 1, "count": len(test.steps), "percent": round(test.step * 100 / len(test.steps))}
    if skill in smart_test.OBJECTIVE:
        items = []
        for i, it in enumerate(smart_test.items_for(step)):
            card = grading.public_item(it)
            random.shuffle(card["opts"])
            card.update(i=i, n=i + 1)
            items.append(card)
        ctx.update(items=items, passages=smart_test.passages_for(step))
    elif skill == "writing":
        ctx["task"] = smart_test.writing_task(request.learner)
    else:
        ctx["sp"] = smart_test.speaking_tasks(request.learner)
    return render(request, "course/level_step.html", ctx)


@paid_required("The level test", "লেভেল টেস্ট")
def level_result(request, pk):
    test = get_object_or_404(SmartTest, pk=pk, learner=request.learner)
    if not test.done:
        return redirect("course:level_step", pk=test.pk)
    rows = []
    for skill in COURSE_SKILLS:
        lv = test.levels.get(skill, 0)
        rows.append({"skill": skill, "name": CourseSkill(skill).label, "bn": SKILL_BN[skill],
                     "emoji": SKILL_EMOJI[skill], "level": lv, "band": test.bands.get(skill, "easy"),
                     "band_bn": BAND_BN.get(test.bands.get(skill, "easy")), "percent": round(lv * 100 / 8),
                     "info": test.scores.get(skill, {})})
    upcoming = path.build_path(request.learner)
    plan = request.learner.plans.filter(is_active=True).first()
    return render(request, "course/level_result.html", {
        "test": test, "rows": rows, "weakest": test.weakest(), "next_up": upcoming[:8],
        "path_total": len(upcoming), "plan": plan, "months": [1, 2, 3, 4, 6, 9, 12],
    })


@require_POST
@paid_required("The skill course (Listening, Speaking, Reading, Writing, Grammar)", "দক্ষতার কোর্স (শোনা, বলা, পড়া, লেখা, ব্যাকরণ)")
def path_plan(request):
    """Turn the course path into the study plan."""
    learner = request.learner
    try:
        months = max(1, min(24, int(request.POST.get("months", 3))))
        days = int(request.POST.get("days_per_week", 5))
        minutes = max(10, min(120, int(request.POST.get("minutes", 20))))
    except ValueError:
        return redirect("course:home")
    lessons = path.build_path(learner)
    feas = planner.course_check(len(lessons), months, days, timezone.localdate())
    if not feas.ok:
        messages.info(request, feas.message)
        return redirect("course:home")
    planner.build_course_plan(learner, lessons, months, days, minutes, timezone.localdate())
    if feas.message != "Good pace.":
        messages.info(request, feas.message)
    messages.success(request, "Your study plan now follows your course path. Finished lessons are kept.")
    return redirect("learning:plan")
