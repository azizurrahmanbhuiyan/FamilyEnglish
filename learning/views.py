import calendar
import random
from datetime import date

from django.contrib import messages
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.utils import learner_required

from . import planner, stats, video
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

def _video_card(lesson, done_ids=(), watch_ids=()):
    """Everything a video thumbnail needs."""
    secs = video.duration_seconds(lesson)
    return {"lesson": lesson, "thumb": video.thumb_for(lesson), "duration": video.duration_label(secs),
            "done": lesson.id in done_ids, "emoji": video.SKILL_EMOJI.get(lesson.skill, "🎬")}


def _lessons_qs():
    return Lesson.objects.select_related("module__level").prefetch_related("items")


@learner_required
def today(request):
    learner = request.learner
    placement = learner.placements.first()
    plan, mission = planner.today_mission(learner, timezone.localdate())
    week = []
    if plan:
        t = timezone.localdate()
        week = plan.days.filter(date__gte=t).select_related("lesson")[:6]
    done_ids = set(Progress.objects.filter(learner=learner).values_list("lesson_id", flat=True))

    # "Up next" videos: the next unfinished lessons in the plan, else in the learner's level.
    if mission:
        up_ids = list(plan.days.filter(status=PlanDay.Status.TODO, lesson__isnull=False)
                      .order_by("date").values_list("lesson_id", flat=True)[:4])
    else:
        start = placement.overall if placement else 0
        up_ids = list(Lesson.objects.filter(module__level__number__gte=start).exclude(id__in=done_ids)
                      .values_list("id", flat=True)[:4])
    by_id = {l.id: l for l in _lessons_qs().filter(id__in=up_ids)}
    up_next = [_video_card(by_id[i], done_ids) for i in up_ids if i in by_id]
    featured = up_next.pop(0) if up_next else None

    return render(request, "learning/today.html", {
        "placement": placement,
        "plan": plan,
        "mission": mission,
        "week": week,
        "featured": featured,
        "up_next": up_next[:3],
        "skills": stats.skill_progress(learner),
        "board": stats.leaderboard(request.family)[:5],
        **stats.learner_stats(learner),
    })


@learner_required
def videos(request):
    """Topic videos: one short video for every lesson, filterable by level and skill."""
    level = request.GET.get("level", "")
    skill = request.GET.get("skill", "")
    qs = _lessons_qs()
    if level.isdigit():
        qs = qs.filter(module__level__number=int(level))
    if skill in Skill.values:
        qs = qs.filter(skill=skill)
    done_ids = set(Progress.objects.filter(learner=request.learner).values_list("lesson_id", flat=True))
    groups, current = [], None
    for lesson in qs:
        lv = lesson.module.level
        if current is None or current["level"].id != lv.id:
            current = {"level": lv, "cards": []}
            groups.append(current)
        current["cards"].append(_video_card(lesson, done_ids))
    return render(request, "learning/videos.html", {
        "groups": groups, "levels": Level.objects.all(), "level": level, "skill": skill,
        "skills": [(v, l, video.SKILL_EMOJI.get(v, "")) for v, l in Skill.choices],
        "count": sum(len(g["cards"]) for g in groups),
    })


@learner_required
def progress(request):
    learner = request.learner
    recent = (Progress.objects.filter(learner=learner).select_related("lesson__module__level")[:8])
    return render(request, "learning/progress.html", {
        "skills": stats.skill_progress(learner),
        "board": stats.leaderboard(request.family),
        "activity": stats.activity(learner),
        "recent": recent,
        "placement": learner.placements.first(),
        "xp_rule": (stats.XP_PER_LESSON, stats.XP_PER_STAR),
        **stats.learner_stats(learner),
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
    skill = request.GET.get("skill", "")
    activity = request.GET.get("activity", "")
    lessons = Lesson.objects.all()
    title = "All lessons"
    if skill in Skill.values:
        lessons = lessons.filter(skill=skill)
        title = f"{Skill(skill).label} lessons"
    if activity in Lesson.Activity.values:
        lessons = lessons.filter(activity=activity)
        title = "Word dictation" if activity == Lesson.Activity.DICTATION else Lesson.Activity(activity).label
    levels = Level.objects.prefetch_related(
        Prefetch("modules__lessons", queryset=lessons, to_attr="shown"))
    levels = [lv for lv in levels if any(m.shown for m in lv.modules.all())]
    done_ids = set(Progress.objects.filter(learner=request.learner).values_list("lesson_id", flat=True))
    return render(request, "learning/library.html", {
        "levels": levels, "done_ids": done_ids, "title": title, "skill": skill, "activity": activity,
        "filtered": bool(skill or activity),
    })


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
    scenes = video.build_scenes(lesson)
    return render(request, "learning/lesson.html", {
        "lesson": lesson, "view": view, "progress": progress,
        "items": lesson.items.all(), "videos": lesson.videos.all(), "next_id": nxt,
        "scenes": scenes, "duration": video.duration_label(round(sum(x["ms"] for x in scenes) / 1000)),
        "thumb": video.thumb_for(lesson),
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
