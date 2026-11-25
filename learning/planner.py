"""Rules-based study planner (no AI): split lessons over the chosen months.

lessons_needed = lessons in every level from start to finish level + review days
study_days     = study dates between start and end on the chosen weekdays
per_day        = lessons_needed / study_days
  > 2   -> too fast: ask for more months or a lower target
  < 0.5 -> slow: suggest a higher target
"""

from dataclasses import dataclass
from datetime import date, timedelta

from django.db import transaction

from .models import Lesson, PlanDay, Progress, StudyPlan

REVIEW_EVERY = 6          # one review day after every 6 lessons
MAX_PER_DAY = 2.0
MIN_PER_DAY = 0.5
FRIDAY = 4                # Python weekday(): Mon=0 ... Sun=6

# Bangladesh school week starts on Sunday; Friday is the family day.
WEEKDAY_SETS = {
    3: [6, 1, 3],                 # Sun, Tue, Thu
    4: [6, 0, 1, 2],              # Sun-Wed
    5: [6, 0, 1, 2, 3],           # Sun-Thu
    6: [5, 6, 0, 1, 2, 3],        # Sat-Thu
}


@dataclass
class Feasibility:
    lessons: int
    review_days: int
    study_days: int
    per_day: float
    ok: bool
    message: str


def add_months(d: date, months: int) -> date:
    year = d.year + (d.month - 1 + months) // 12
    month = (d.month - 1 + months) % 12 + 1
    # clamp the day to the length of the target month
    for day in (d.day, 30, 29, 28):
        try:
            return date(year, month, day)
        except ValueError:
            continue
    return date(year, month, 28)


def lessons_for_range(start_level: int, finish_level: int, exclude_done_for=None):
    qs = Lesson.objects.filter(
        module__level__number__gte=start_level,
        module__level__number__lte=finish_level,
    ).select_related("module__level").order_by("module__level__number", "module__order", "order")
    if exclude_done_for is not None:
        done_ids = Progress.objects.filter(learner=exclude_done_for).values_list("lesson_id", flat=True)
        qs = qs.exclude(id__in=list(done_ids))
    return list(qs)


def study_dates(start: date, end: date, days_per_week: int):
    weekdays = WEEKDAY_SETS.get(days_per_week, WEEKDAY_SETS[5])
    d = start
    while d < end:
        if d.weekday() in weekdays:
            yield d
        d += timedelta(days=1)


def check(start_level, finish_level, months, days_per_week, start=None, learner=None) -> Feasibility:
    start = start or date.today()
    end = add_months(start, months)
    lessons = len(lessons_for_range(start_level, finish_level, exclude_done_for=learner))
    reviews = lessons // REVIEW_EVERY
    days = sum(1 for _ in study_dates(start, end, days_per_week))
    per_day = (lessons + reviews) / days if days else 99.0
    if lessons == 0:
        return Feasibility(0, 0, days, 0, False, "No lessons found for these levels yet.")
    if per_day > MAX_PER_DAY:
        return Feasibility(lessons, reviews, days, per_day, False,
                           "Too fast: choose more months, more study days, or a lower finish level.")
    if per_day < MIN_PER_DAY:
        return Feasibility(lessons, reviews, days, per_day, True,
                           "Comfortable pace. You could aim for a higher finish level.")
    return Feasibility(lessons, reviews, days, per_day, True, "Good pace.")


@transaction.atomic
def build_plan(learner, start_level, finish_level, months, days_per_week=5,
               minutes_per_day=20, start=None) -> StudyPlan:
    """Create a new active plan. Older plans are kept as history but switched off."""
    start = start or date.today()
    end = add_months(start, months)
    feas = check(start_level, finish_level, months, days_per_week, start, learner)
    if not feas.ok:
        raise ValueError(feas.message)

    StudyPlan.objects.filter(learner=learner, is_active=True).update(is_active=False)
    plan = StudyPlan.objects.create(
        learner=learner, start_level=start_level, target_level=finish_level, months=months,
        days_per_week=days_per_week, minutes_per_day=minutes_per_day,
        start_date=start, end_date=end,
    )

    # Sequence of items: lessons with a review day after every REVIEW_EVERY lessons
    items = []
    for i, lesson in enumerate(lessons_for_range(start_level, finish_level, exclude_done_for=learner), 1):
        items.append(("lesson", lesson))
        if i % REVIEW_EVERY == 0:
            items.append(("review", None))

    dates = list(study_dates(start, end, days_per_week))
    n_days, n_items = len(dates), len(items)
    rows = []
    # Spread items evenly: item i goes to day floor(i * n_days / n_items)
    for i, (kind, lesson) in enumerate(items):
        rows.append(PlanDay(plan=plan, date=dates[i * n_days // n_items], lesson=lesson, kind=kind))

    # One family-practice day every Friday inside the plan
    d = start
    while d < end:
        if d.weekday() == FRIDAY:
            rows.append(PlanDay(plan=plan, date=d, kind="family"))
        d += timedelta(days=1)

    PlanDay.objects.bulk_create(rows)
    return plan


def today_mission(learner, today=None):
    """The first unfinished lesson day on or before today; else the next one."""
    today = today or date.today()
    plan = learner.plans.filter(is_active=True).first()
    if not plan:
        return None, None
    todo = plan.days.filter(status=PlanDay.Status.TODO, kind__in=["lesson", "course"]).select_related(
        "lesson__module__level", "course_lesson")
    if plan.kind == "track":   # full courses: the first open day of any kind (new, talk or repeat)
        todo = plan.days.filter(status=PlanDay.Status.TODO).exclude(kind="family").select_related(
            "lesson__module__level", "course_lesson", "topic", "deck")
    day = todo.filter(date__lte=today).first() or todo.first()
    return plan, day


def mark_lesson_done(learner, lesson, score=0):
    from growth.engine import award

    stars = 3 if score >= 80 else 2 if score >= 50 else 1
    prog, created = Progress.objects.get_or_create(learner=learner, lesson=lesson,
                                                   defaults={"stars": stars, "score": score})
    if not created and score > prog.score:
        prog.score, prog.stars = score, stars
        prog.save()
    award(learner, 20, "lesson", key=f"lesson-{lesson.id}")
    for n in range(1, prog.stars + 1):
        award(learner, 10, "lesson stars", key=f"lesson-{lesson.id}-s{n}")
    tick_days(learner, lesson=lesson)
    return prog


def course_check(lessons_count, months, days_per_week, start=None):
    start = start or date.today()
    end = add_months(start, months)
    days = sum(1 for _ in study_dates(start, end, days_per_week))
    reviews = lessons_count // REVIEW_EVERY
    per_day = (lessons_count + reviews) / days if days else 99.0
    fits = int(days * MAX_PER_DAY * REVIEW_EVERY / (REVIEW_EVERY + 1))
    if lessons_count == 0:
        return Feasibility(0, 0, days, 0, False, "Every lesson in your path is already passed. Well done!")
    if per_day > MAX_PER_DAY:
        return Feasibility(lessons_count, reviews, days, per_day, True,
                           f"That is a lot for {months} month(s): the plan will include the first {fits} "
                           "lessons of your path. Choose more months to fit them all.")
    return Feasibility(lessons_count, reviews, days, per_day, True, "Good pace.")


@transaction.atomic
def build_course_plan(learner, lessons, months, days_per_week=5, minutes_per_day=20, start=None):
    """A plan made from the AI-test course path (course.path.build_path)."""
    start = start or date.today()
    end = add_months(start, months)
    dates = list(study_dates(start, end, days_per_week))
    if not dates or not lessons:
        raise ValueError("Nothing to plan.")
    max_lessons = int(len(dates) * MAX_PER_DAY * REVIEW_EVERY / (REVIEW_EVERY + 1))
    lessons = list(lessons)[:max_lessons]
    StudyPlan.objects.filter(learner=learner, is_active=True).update(is_active=False)
    levels = learner.placements.first()
    lv = levels.overall if levels else 0
    plan = StudyPlan.objects.create(
        learner=learner, start_level=lv, target_level=min(8, lv + 2), months=months, kind="course",
        days_per_week=days_per_week, minutes_per_day=minutes_per_day, start_date=start, end_date=end)
    items = []
    for i, lesson in enumerate(lessons, 1):
        items.append(("course", lesson))
        if i % REVIEW_EVERY == 0:
            items.append(("review", None))
    n_days, n_items = len(dates), len(items)
    rows = [PlanDay(plan=plan, date=dates[i * n_days // n_items], course_lesson=l, kind=k)
            for i, (k, l) in enumerate(items)]
    d = start
    while d < end:
        if d.weekday() == FRIDAY:
            rows.append(PlanDay(plan=plan, date=d, kind="family"))
        d += timedelta(days=1)
    PlanDay.objects.bulk_create(rows)
    return plan


def restart_plan(learner, today=None):
    """Rebuild the active plan from today with the same settings. Finished work is kept."""
    today = today or date.today()
    plan = learner.plans.filter(is_active=True).first()
    if not plan:
        return None
    if plan.kind == "course":
        from course.path import build_path
        return build_course_plan(learner, build_path(learner), plan.months, plan.days_per_week,
                                 plan.minutes_per_day, today)
    feas = check(plan.start_level, plan.target_level, plan.months, plan.days_per_week, today, learner)
    if not feas.ok:
        raise ValueError(feas.message)
    return build_plan(learner, plan.start_level, plan.target_level, plan.months, plan.days_per_week,
                      plan.minutes_per_day, today)


def week_focus(plan, today=None):
    """Tasks per skill in this week (Sunday to Saturday) and how many are done."""
    today = today or date.today()
    start = today - timedelta(days=(today.weekday() + 1) % 7)
    days = list(plan.days.filter(date__gte=start, date__lt=start + timedelta(days=7))
                .select_related("lesson", "course_lesson"))
    focus = {}
    for d in days:
        skill = (d.course_lesson.skill if d.course_lesson_id else d.lesson.skill if d.lesson_id else d.kind)
        focus[skill] = focus.get(skill, 0) + 1
    lesson_days = [d for d in days if d.kind in ("lesson", "course")]
    return {"focus": sorted(focus.items(), key=lambda x: -x[1]),
            "done": sum(1 for d in lesson_days if d.status == PlanDay.Status.DONE),
            "total": len(lesson_days),
            "minutes": sum(plan.minutes_per_day for d in lesson_days if d.status == PlanDay.Status.DONE)}


def streak(learner, today=None):
    """Consecutive days (ending today or yesterday) with at least one finished lesson."""
    today = today or date.today()
    from django.utils import timezone

    days = {timezone.localtime(p.completed_at).date()
            for p in Progress.objects.filter(learner=learner)}
    d = today if today in days else today - timedelta(days=1)
    count = 0
    while d in days:
        count += 1
        d -= timedelta(days=1)
    return count


def tick_days(learner, **item):
    """Finishing an item ticks its 'new lesson' day, and the next repeat day that is due."""
    from django.utils import timezone

    days = PlanDay.objects.filter(plan__learner=learner, plan__is_active=True, **item)
    days.exclude(kind="review").update(status=PlanDay.Status.DONE)
    due = days.filter(kind="review", status=PlanDay.Status.TODO, date__lte=timezone.localdate()).first()
    if due:
        due.status = PlanDay.Status.DONE
        due.save(update_fields=["status"])
