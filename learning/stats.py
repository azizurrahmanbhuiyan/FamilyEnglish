"""XP, skill progress and the family leaderboard for the dashboard."""

from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from . import planner
from .models import Lesson, Progress, Skill
from .video import SKILL_EMOJI

XP_PER_LESSON = 20
XP_PER_STAR = 10


def xp_of(progress_rows):
    return sum(XP_PER_LESSON + XP_PER_STAR * p.stars for p in progress_rows)


def learner_stats(learner):
    """XP comes from the XP ledger (lessons, course self-tests, flashcards, speaking, writing…)."""
    from course.models import CourseProgress
    from growth import engine

    rows = list(Progress.objects.filter(learner=learner))
    course = list(CourseProgress.objects.filter(learner=learner, passed=True))
    t = engine.totals(learner)
    info = engine.streak_info(learner)
    return {
        "xp": t["xp"],
        "week_xp": t["week_xp"],
        "stars": sum(p.stars for p in rows) + sum(c.stars for c in course),
        "done_count": len(rows) + len(course),
        "streak": info["streak"],
        "freezes_left": info["freezes_left"],
    }


def skill_progress(learner):
    """Lessons done / total for each skill, with a percentage for the bar."""
    totals = dict(Lesson.objects.values_list("skill").annotate(n=Count("id")))
    done = dict(Progress.objects.filter(learner=learner).values_list("lesson__skill")
                .annotate(n=Count("id")))
    out = []
    for value, label in Skill.choices:
        total = totals.get(value, 0)
        if not total:
            continue
        d = done.get(value, 0)
        out.append({"skill": value, "label": label, "emoji": SKILL_EMOJI.get(value, "📘"),
                    "done": d, "total": total, "percent": round(d * 100 / total)})
    return out


def leaderboard(family):
    """Family members ranked by XP earned in the last 7 days."""
    board = []
    for learner in family.learners.all():
        s = learner_stats(learner)
        board.append({"learner": learner, **s})
    board.sort(key=lambda r: (-r["week_xp"], -r["xp"], r["learner"].name))
    for i, r in enumerate(board, 1):
        r["rank"] = i
        r["medal"] = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, str(i))
    return board


def activity(learner, days=28):
    """Learning activities per day (lessons, tests, cards, practice) for the last `days` days."""
    from growth.models import XPEvent

    today = timezone.localdate()
    counts = {}
    for t in XPEvent.objects.filter(learner=learner, created_at__gte=timezone.now() - timedelta(days=days + 1)
                                    ).values_list("created_at", flat=True):
        d = timezone.localtime(t).date()
        counts[d] = counts.get(d, 0) + 1
    out = []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        n = counts.get(d, 0)
        out.append({"date": d, "n": n, "shade": 0 if n == 0 else 1 if n <= 2 else 2 if n <= 5 else 3})
    return out
