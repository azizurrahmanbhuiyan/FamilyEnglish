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
    rows = list(Progress.objects.filter(learner=learner))
    week_start = timezone.now() - timedelta(days=7)
    return {
        "xp": xp_of(rows),
        "week_xp": xp_of(p for p in rows if p.completed_at >= week_start),
        "stars": sum(p.stars for p in rows),
        "done_count": len(rows),
        "streak": planner.streak(learner, timezone.localdate()),
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
    """Lessons finished per day for the last `days` days (oldest first)."""
    today = timezone.localdate()
    counts = {}
    for p in Progress.objects.filter(learner=learner,
                                     completed_at__gte=timezone.now() - timedelta(days=days + 1)):
        d = timezone.localtime(p.completed_at).date()
        counts[d] = counts.get(d, 0) + 1
    out = []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        n = counts.get(d, 0)
        out.append({"date": d, "n": n, "shade": 0 if n == 0 else 1 if n == 1 else 2 if n == 2 else 3})
    return out
