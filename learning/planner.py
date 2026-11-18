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
    todo = plan.days.filter(status=PlanDay.Status.TODO, kind="lesson").select_related(
        "lesson__module__level")
    day = todo.filter(date__lte=today).first() or todo.first()
    return plan, day


def mark_lesson_done(learner, lesson, score=0):
    stars = 3 if score >= 80 else 2 if score >= 50 else 1
    prog, created = Progress.objects.get_or_create(learner=learner, lesson=lesson,
                                                   defaults={"stars": stars, "score": score})
    if not created and score > prog.score:
        prog.score, prog.stars = score, stars
        prog.save()
    PlanDay.objects.filter(plan__learner=learner, plan__is_active=True, lesson=lesson).update(
        status=PlanDay.Status.DONE)
    return prog


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
