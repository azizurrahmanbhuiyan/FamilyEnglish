import calendar
import random
from datetime import date

from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.utils import learner_required

from . import planner
from .forms import PlanForm
from .models import (Lesson, Level, PlacementQuestion, PlanDay, Progress, Skill)
from .placement import (READER_MAX, READER_MIN, SPEAKING_CAN_DO, save_placement,
                        score_reader, score_young_child)


def _shuffled(questions):
    """Attach shuffled choices so the right answer is not always in the same place."""
    out = list(questions)
    for q in out:
        q.shuffled = random.sample(q.choice_list(), len(q.choice_list()))
    return out


def _can_open(family, lesson):
    """Free accounts after the trial can open the first module of every level."""
    return family.has_full_access or lesson.module.order == 1


# ---------- Today ----------

@learner_required
def today(request):
    learner = request.learner
    placement = learner.placements.first()
    plan, mission = planner.today_mission(learner, timezone.localdate())
    week = []
    if plan:
        t = timezone.localdate()
        week = plan.days.filter(date__gte=t).select_related("lesson")[:8]
    return render(request, "learning/today.html", {
        "placement": placement,
        "plan": plan,
        "mission": mission,
        "week": week,
        "streak": planner.streak(learner),
        "stars": sum(Progress.objects.filter(learner=learner).values_list("stars", flat=True)),
        "done_count": Progress.objects.filter(learner=learner).count(),
    })


# ---------- Placement ----------

@learner_required
def placement_start(request):
    learner = request.learner
    suggested = "young" if (learner.is_young_child or (learner.age is not None and learner.age < 7)) else "reader"
    return render(request, "learning/placement_start.html", {"suggested": suggested})


@learner_required
def placement_young(request):
    questions = PlacementQuestion.objects.filter(skill=Skill.PHONICS, level__lte=2)
    if request.method == "POST":
        level = score_young_child(request.POST)
        p = save_placement(request.learner, {s: level for s in
                                             ("listening", "speaking", "reading", "writing")}, young=True)
        return redirect("learning:placement_result", pk=p.pk)
    return render(request, "learning/placement_young.html", {"questions": _shuffled(questions)})


@learner_required
def placement_reader(request):
    qs = PlacementQuestion.objects.filter(level__gte=READER_MIN, level__lte=READER_MAX).exclude(
        skill=Skill.PHONICS)
    sections = [
        ("listening", "Listening", "শুনুন, তারপর উত্তর দিন। ▶ চাপলে বাক্যটি শোনা যাবে।", _shuffled(qs.filter(skill="listening"))),
        ("reading", "Reading", "পড়ুন, তারপর উত্তর দিন।", _shuffled(qs.filter(skill="reading"))),
        ("writing", "Writing (grammar)", "সঠিক শব্দটি বেছে নিন।", _shuffled(qs.filter(skill="writing"))),
    ]
    if request.method == "POST":
        # Speaking: the highest can-do statement ticked (parent answers for a child)
        ticked = [int(v) for v in request.POST.getlist("can_do") if v.isdigit()]
        speaking = max(ticked) if ticked else 2
        levels = score_reader(request.POST, speaking)
        p = save_placement(request.learner, levels)
        return redirect("learning:placement_result", pk=p.pk)
    return render(request, "learning/placement_reader.html",
                  {"sections": sections, "can_do": SPEAKING_CAN_DO})


@learner_required
def placement_result(request, pk):
    p = get_object_or_404(request.learner.placements, pk=pk)
    levels = {lv.number: lv for lv in Level.objects.all()}
    skills = [(name.title(), value, levels.get(value)) for name, value in p.skill_levels().items()]
    return render(request, "learning/placement_result.html", {
        "p": p, "skills": skills, "overall": levels.get(p.overall),
        "weakest": p.weakest_skill(),
    })


# ---------- Study plan ----------

@learner_required
def plan_new(request):
    learner = request.learner
    placement = learner.placements.first()
    start_level = min(placement.skill_levels().values()) if placement else 0
    initial = {"start_level": start_level, "finish_level": min(start_level + 1, 8),
               "months": 3, "days_per_week": 5, "minutes_per_day": 20}
    form = PlanForm(request.POST or None, initial=initial)
    feas = None
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        feas = planner.check(d["start_level"], d["finish_level"], d["months"], d["days_per_week"],
                             timezone.localdate(), learner)
        if "create" in request.POST and feas.ok:
            planner.build_plan(learner, d["start_level"], d["finish_level"], d["months"],
                               d["days_per_week"], d["minutes_per_day"], timezone.localdate())
            messages.success(request, "Your study plan is ready. Finished lessons are kept.")
            return redirect("learning:plan")
    return render(request, "learning/plan_new.html", {"form": form, "feas": feas,
                                                      "placement": placement})


@learner_required
def plan_calendar(request):
    plan = request.learner.plans.filter(is_active=True).first()
    if not plan:
        return redirect("learning:plan_new")
    today = timezone.localdate()
    try:
        year = int(request.GET.get("y", today.year))
        month = int(request.GET.get("m", today.month))
        date(year, month, 1)
    except ValueError:
        raise Http404
    by_date = {}
    for d in plan.days.filter(date__year=year, date__month=month).select_related("lesson"):
        by_date.setdefault(d.date, []).append(d)
    cal = calendar.Calendar(firstweekday=6)  # Sunday first
    weeks = [[(day, by_date.get(day, [])) for day in week] for week in cal.monthdatescalendar(year, month)]
    prev_m = (year, month - 1) if month > 1 else (year - 1, 12)
    next_m = (year, month + 1) if month < 12 else (year + 1, 1)
    done, total = plan.progress()
    return render(request, "learning/plan.html", {
        "plan": plan, "weeks": weeks, "month_name": calendar.month_name[month], "year": year,
        "month": month, "prev_m": prev_m, "next_m": next_m, "today": today,
        "done": done, "total": total, "percent": round(done * 100 / total) if total else 0,
    })


# ---------- Library and lessons ----------

@learner_required
def library(request):
    levels = Level.objects.prefetch_related("modules__lessons")
    done_ids = set(Progress.objects.filter(learner=request.learner).values_list("lesson_id", flat=True))
    return render(request, "learning/library.html", {"levels": levels, "done_ids": done_ids})


@learner_required
def lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson.objects.select_related("module__level"), pk=pk)
    if not _can_open(request.family, lesson):
        messages.info(request, "This lesson is part of the Family plan. One plan covers everyone "
                               "in the family — any adult can buy it.")
        return redirect("core:pricing")
    view = request.GET.get("view") or ("kid" if request.learner.role == "child" else "parent")
    progress = Progress.objects.filter(learner=request.learner, lesson=lesson).first()
    ordered = list(Lesson.objects.filter(module__level=lesson.module.level).order_by(
        "module__order", "order").values_list("id", flat=True))
    idx = ordered.index(lesson.id)
    nxt = ordered[idx + 1] if idx + 1 < len(ordered) else None
    return render(request, "learning/lesson.html", {
        "lesson": lesson, "view": view, "progress": progress,
        "items": lesson.items.all(), "videos": lesson.videos.all(), "next_id": nxt,
    })


@require_POST
@learner_required
def lesson_complete(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    try:
        score = max(0, min(100, int(request.POST.get("score", "0"))))
    except ValueError:
        score = 0
    prog = planner.mark_lesson_done(request.learner, lesson, score)
    messages.success(request, f"{'⭐' * prog.stars} Well done, {request.learner.name}! "
                              "Don't forget today's home task.")
    return redirect("learning:today")


@require_POST
@learner_required
def day_done(request, pk):
    """Tick off a review or family-practice day."""
    day = get_object_or_404(PlanDay, pk=pk, plan__learner=request.learner)
    day.status = PlanDay.Status.DONE
    day.save()
    return redirect(request.POST.get("next") or "learning:plan")
