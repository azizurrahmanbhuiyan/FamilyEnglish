"""XP, streaks (with freezes), daily goals, badges and weekly leagues."""

from datetime import timedelta

from django.db import IntegrityError, transaction
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from .models import LeagueState, LearnerGoal, XPEvent

FREEZES_PER_MONTH = 3

LEAGUES = [
    ("bronze", "Bronze", "🥉"),
    ("silver", "Silver", "🥈"),
    ("gold", "Gold", "🥇"),
    ("diamond", "Diamond", "💎"),
]
LEAGUE_KEYS = [k for k, _, _ in LEAGUES]
LEAGUE_NAME = {k: n for k, n, _ in LEAGUES}
LEAGUE_ICON = {k: i for k, _, i in LEAGUES}
PROMOTE = 3       # top 3 move up each week
DEMOTE = 3        # bottom 3 move down (only learners who earned no XP, so nobody is punished for trying)


# ------------------------------------------------------------------ XP

def award(learner, amount, reason, key=None, when=None):
    """Give XP once per key. Returns True if XP was added."""
    if not learner or amount <= 0:
        return False
    try:
        with transaction.atomic():
            XPEvent.objects.create(learner=learner, amount=amount, reason=reason[:60], key=key,
                                   created_at=when or timezone.now())
        return True
    except IntegrityError:
        return False


def xp_today(learner, reason=None):
    start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    qs = learner.xp_events.filter(created_at__gte=start)
    if reason:
        qs = qs.filter(reason=reason)
    return qs.aggregate(n=Sum("amount"))["n"] or 0


def week_start(day=None):
    """Weeks run Sunday to Saturday (the Bangladesh school week)."""
    day = day or timezone.localdate()
    return day - timedelta(days=(day.weekday() + 1) % 7)


def _local_start(day):
    return timezone.make_aware(timezone.datetime.combine(day, timezone.datetime.min.time()))


def xp_between(learner_ids, start_day, end_day):
    rows = (XPEvent.objects.filter(learner_id__in=learner_ids, created_at__gte=_local_start(start_day),
                                   created_at__lt=_local_start(end_day))
            .values("learner_id").annotate(n=Sum("amount")))
    return {r["learner_id"]: r["n"] for r in rows}


def totals(learner):
    ws = week_start()
    agg = learner.xp_events.aggregate(
        total=Sum("amount"), week=Sum("amount", filter=Q(created_at__gte=_local_start(ws))))
    return {"xp": agg["total"] or 0, "week_xp": agg["week"] or 0}


# ------------------------------------------------------------------ streaks

def active_days(learner, since=None):
    qs = learner.xp_events.all()
    if since:
        qs = qs.filter(created_at__gte=_local_start(since))
    return {timezone.localtime(t).date() for t in qs.values_list("created_at", flat=True)}


def streak_info(learner, today=None):
    """Current streak, freezes used this month and the best streak ever.

    A missed day is covered automatically by a streak freeze (3 per calendar month). Frozen days
    keep the streak alive but do not add to it. Today does not break the streak until it is over.
    """
    today = today or timezone.localdate()
    days = active_days(learner)
    bought = _bought_freezes(learner)
    used = {}            # month -> freezes used
    frozen = []
    d = today if today in days else today - timedelta(days=1)
    count, gap = 0, []
    first_day = min(days) if days else today
    while True:
        if d in days:
            count += 1
            frozen += gap
            gap = []
        else:
            month = (d.year, d.month)
            if d < first_day or used.get(month, 0) >= FREEZES_PER_MONTH + bought.get(month, 0):
                for g in gap:  # this gap was too long: its freezes were not really used
                    used[(g.year, g.month)] -= 1
                break
            used[month] = used.get(month, 0) + 1
            gap.append(d)
        d -= timedelta(days=1)
    this_month = used.get((today.year, today.month), 0)
    allowance = FREEZES_PER_MONTH + bought.get((today.year, today.month), 0)
    return {"streak": count, "frozen_days": sorted(frozen), "freezes_left": allowance - this_month,
            "freezes_used": this_month, "best": max(count, best_streak(days)),
            "active_today": today in days}


def _bought_freezes(learner):
    """Extra streak freezes bought with gems in the studio: {(year, month): n}."""
    w = getattr(learner, "wallet", None) if learner else None
    try:
        if w and w.extra_freezes and w.freeze_month:
            y, m = w.freeze_month.split("-")
            return {(int(y), int(m)): w.extra_freezes}
    except (ValueError, AttributeError):
        pass
    return {}


def best_streak(days):
    best = run = 0
    prev = None
    for d in sorted(days):
        run = run + 1 if prev and d - prev == timedelta(days=1) else 1
        best = max(best, run)
        prev = d
    return best


def heatmap(learner, days=182):
    """XP per day for the last `days` days, oldest first, in whole weeks (Sunday first)."""
    today = timezone.localdate()
    start = week_start(today - timedelta(days=days - 1))
    rows = (learner.xp_events.filter(created_at__gte=_local_start(start))
            .annotate(d=TruncDate("created_at", tzinfo=timezone.get_current_timezone()))
            .values("d").annotate(n=Sum("amount")))
    per = {r["d"]: r["n"] for r in rows}
    weeks, d = [], start
    while d <= today:
        week = []
        for _ in range(7):
            n = per.get(d, 0) if d <= today else None
            shade = None if n is None else 0 if n == 0 else 1 if n < 20 else 2 if n < 50 else 3
            week.append({"date": d, "xp": n, "shade": shade})
            d += timedelta(days=1)
        weeks.append(week)
    return weeks


def consistency(learner, days=14):
    today = timezone.localdate()
    active = active_days(learner, since=today - timedelta(days=days))
    out = [{"date": today - timedelta(days=i), "on": (today - timedelta(days=i)) in active}
           for i in range(days - 1, -1, -1)]
    return out, sum(1 for x in out if x["on"])


# ------------------------------------------------------------------ goals

def goal_for(learner):
    goal, _ = LearnerGoal.objects.get_or_create(learner=learner)
    return goal


def today_progress(learner):
    from course.models import AnswerLog, CourseProgress
    from learning.models import Progress

    start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    goal = goal_for(learner)
    xp = xp_today(learner)
    questions = AnswerLog.objects.filter(learner=learner, created_at__gte=start).count()
    lessons = (CourseProgress.objects.filter(learner=learner, passed_at__gte=start).count()
               + Progress.objects.filter(learner=learner, completed_at__gte=start).count())
    rows = [
        {"key": "xp", "label": "XP", "label_bn": "XP", "now": xp, "target": goal.xp, "icon": "⚡"},
        {"key": "questions", "label": "Questions", "label_bn": "প্রশ্ন", "now": questions,
         "target": goal.questions, "icon": "❓"},
        {"key": "lessons", "label": "Lessons", "label_bn": "পাঠ", "now": lessons, "target": goal.lessons,
         "icon": "📘"},
    ]
    for r in rows:
        r["percent"] = min(100, round(r["now"] * 100 / r["target"])) if r["target"] else 100
        r["done"] = r["now"] >= r["target"]
    return rows


# ------------------------------------------------------------------ badges

def badge_stats(learner):
    from course.models import AnswerLog, CourseProgress, SelfTestAttempt
    from learning.models import Progress
    from practice.models import LEARNED_BOX, CardReview

    passed = CourseProgress.objects.filter(learner=learner, passed=True)
    t = totals(learner)
    info = streak_info(learner)
    return {
        "lessons": passed.count() + Progress.objects.filter(learner=learner).count(),
        "grammar": passed.filter(lesson__skill="grammar").count(),
        "skills": passed.values("lesson__skill").distinct().count(),
        "perfect": SelfTestAttempt.objects.filter(learner=learner, percent=100).count(),
        "best_streak": info["best"],
        "xp": t["xp"],
        "words": CardReview.objects.filter(learner=learner, box__gte=LEARNED_BOX).count(),
        "speaking": learner.speaking_attempts.count(),
        "writing": learner.writing_attempts.count(),
        "smart": learner.smart_tests.filter(finished_at__isnull=False).count(),
        "answers": AnswerLog.objects.filter(learner=learner, correct=True).count(),
        "advanced": passed.filter(lesson__band="advanced").count(),
    }


BADGES = [
    ("first_lesson", "🌱", "First step", "প্রথম পদক্ষেপ", "Finish your first lesson", "lessons", 1),
    ("test_taker", "🧠", "Level found", "লেভেল জানা হলো", "Take the AI level test", "smart", 1),
    ("streak3", "🔥", "3-day streak", "৩ দিনের ধারা", "Learn 3 days in a row", "best_streak", 3),
    ("streak7", "🔥", "Week warrior", "সপ্তাহ বীর", "Learn 7 days in a row", "best_streak", 7),
    ("streak30", "🏅", "Month master", "মাসের সেরা", "Learn 30 days in a row", "best_streak", 30),
    ("lessons10", "📘", "Ten lessons", "দশটি পাঠ", "Finish 10 lessons", "lessons", 10),
    ("lessons50", "📚", "Bookworm", "বইপোকা", "Finish 50 lessons", "lessons", 50),
    ("all_skills", "🌈", "All-rounder", "সব দিকেই দক্ষ", "Pass a lesson in all 5 skills", "skills", 5),
    ("grammar5", "🧩", "Grammar builder", "ব্যাকরণ নির্মাতা", "Pass 5 grammar lessons", "grammar", 5),
    ("perfect", "💯", "Perfect score", "পূর্ণ নম্বর", "Get 100% in a self-test", "perfect", 1),
    ("words100", "🃏", "Word collector", "শব্দ সংগ্রাহক", "Learn 100 flashcard words", "words", 100),
    ("speaker", "🎤", "Brave speaker", "সাহসী বক্তা", "Do 10 speaking practices", "speaking", 10),
    ("writer", "📝", "Busy writer", "লেখক", "Check 10 pieces of writing", "writing", 10),
    ("xp500", "⚡", "500 XP", "৫০০ XP", "Earn 500 XP", "xp", 500),
    ("advanced", "🚀", "Advanced learner", "উচ্চতর শিক্ষার্থী", "Pass 3 Advanced lessons", "advanced", 3),
]


def badges(learner, stats=None):
    stats = stats or badge_stats(learner)
    out = []
    for key, icon, name, name_bn, desc, stat, target in BADGES:
        now = stats.get(stat, 0)
        out.append({"key": key, "icon": icon, "name": name, "name_bn": name_bn, "desc": desc,
                    "now": min(now, target), "target": target, "earned": now >= target,
                    "percent": min(100, round(now * 100 / target))})
    return out


def next_badge(all_badges):
    pending = [b for b in all_badges if not b["earned"]]
    return max(pending, key=lambda b: b["percent"]) if pending else None


# ------------------------------------------------------------------ leagues

def settle_leagues(today=None):
    """Once a week, move the top learners of each league up and inactive bottom learners down."""
    from core.models import Learner

    this_week = week_start(today)
    state, _ = LeagueState.objects.get_or_create(pk=1)
    if state.last_settled and state.last_settled >= this_week:
        return False
    last_week = this_week - timedelta(days=7)
    members = {key: list(Learner.objects.filter(league=key).values_list("id", flat=True)) for key in LEAGUE_KEYS}
    for i, key in enumerate(LEAGUE_KEYS):
        ids = members[key]  # snapshot, so nobody moves more than one league in a week
        if not ids:
            continue
        xp = xp_between(ids, last_week, this_week)
        ranked = sorted(ids, key=lambda lid: -xp.get(lid, 0))
        if i < len(LEAGUE_KEYS) - 1:
            up = [lid for lid in ranked[:PROMOTE] if xp.get(lid, 0) > 0]
            Learner.objects.filter(id__in=up).update(league=LEAGUE_KEYS[i + 1])
        if i > 0 and len(ranked) > 5:
            down = [lid for lid in ranked[-DEMOTE:] if xp.get(lid, 0) == 0]
            Learner.objects.filter(id__in=down).update(league=LEAGUE_KEYS[i - 1])
    state.last_settled = this_week
    state.save()
    return True


def league_board(learner, limit=30):
    """This week's table for the learner's league. Other families only see avatar + nickname."""
    from core.models import Learner

    settle_leagues()
    learner.refresh_from_db(fields=["league"])
    members = list(Learner.objects.filter(league=learner.league).select_related("family"))
    ws = week_start()
    xp = xp_between([m.id for m in members], ws, ws + timedelta(days=7))
    rows = []
    for m in members:
        rows.append({"learner": m, "xp": xp.get(m.id, 0), "me": m.id == learner.id,
                     "family": m.family_id == learner.family_id})
    rows.sort(key=lambda r: (-r["xp"], r["learner"].id))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
        r["zone"] = ("up" if i <= PROMOTE and r["xp"] > 0 and learner.league != LEAGUE_KEYS[-1]
                     else "down" if i > len(rows) - DEMOTE and len(rows) > 5 and r["xp"] == 0
                     and learner.league != LEAGUE_KEYS[0] else "")
    mine = next((r for r in rows if r["me"]), None)
    return rows[:limit], mine, len(rows)


def xp_panel(learner):
    t = totals(learner)
    _, mine, size = league_board(learner, limit=0)
    return {**t, "league": learner.league, "league_name": LEAGUE_NAME.get(learner.league, "Bronze"),
            "league_icon": LEAGUE_ICON.get(learner.league, "🥉"), "rank": mine["rank"] if mine else None,
            "size": size, "today": xp_today(learner)}


def practice_mix(learner, days=30):
    from course.models import AnswerLog

    since = timezone.now() - timedelta(days=days)
    rows = (AnswerLog.objects.filter(learner=learner, created_at__gte=since).exclude(skill="")
            .values("skill").annotate(n=Count("id")))
    total = sum(r["n"] for r in rows) or 1
    return [{"skill": r["skill"], "n": r["n"], "percent": round(r["n"] * 100 / total)}
            for r in sorted(rows, key=lambda r: -r["n"])]
