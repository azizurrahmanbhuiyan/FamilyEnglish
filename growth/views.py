import calendar
from datetime import timedelta

from django.contrib import messages
from django.contrib.sessions.models import Session
from django.db.models import Avg, Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from core.models import Learner, UserDevice
from core.utils import family_required, learner_required
from learning import stats

from . import engine
from .changelog import CHANGES
from .models import FeatureIdea, FeatureVote, XPEvent


def set_language(request, code):
    from world.data import is_language
    if is_language(code):
        request.session["lang"] = code
        if request.user.is_authenticated:
            from world.models import profile_for
            p = profile_for(request.user)
            p.language = code
            p.save(update_fields=["language"])
    nxt = request.GET.get("next") or request.META.get("HTTP_REFERER") or "/"
    if not url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        nxt = "/"
    return redirect(nxt)


# ------------------------------------------------------------------ streaks, goals, badges

def _summary(learner, since):
    from course.models import AnswerLog

    qs = learner.xp_events.all()
    answers = AnswerLog.objects.filter(learner=learner)
    if since:
        qs = qs.filter(created_at__gte=since)
        answers = answers.filter(created_at__gte=since)
    days = {timezone.localtime(t).date() for t in qs.values_list("created_at", flat=True)}
    n = answers.count()
    right = answers.filter(correct=True).count()
    return {"xp": qs.aggregate(s=Sum("amount"))["s"] or 0, "days": len(days), "answers": n,
            "accuracy": round(right * 100 / n) if n else None}


def _score_trend(learner):
    from course.models import COURSE_SKILLS, SKILL_EMOJI, SelfTestAttempt

    out = []
    for skill in COURSE_SKILLS:
        rows = list(SelfTestAttempt.objects.filter(learner=learner, lesson__skill=skill)
                    .order_by("-created_at")[:10])[::-1]
        if rows:
            out.append({"skill": skill, "emoji": SKILL_EMOJI[skill], "points": [r.percent for r in rows],
                        "avg": round(sum(r.percent for r in rows) / len(rows)), "last": rows[-1].percent})
    return out


@learner_required
def streaks(request):
    learner = request.learner
    info = engine.streak_info(learner)
    today = timezone.localdate()
    active = engine.active_days(learner, since=today.replace(day=1) - timedelta(days=7))
    cal = calendar.Calendar(firstweekday=6)
    month = [[{"date": d, "in": d.month == today.month, "on": d in active, "frozen": d in info["frozen_days"],
               "today": d == today, "future": d > today} for d in week]
             for week in cal.monthdatescalendar(today.year, today.month)]
    all_badges = engine.badges(learner)
    now = timezone.now()
    return render(request, "growth/streaks.html", {
        "info": info, "month": month, "month_name": calendar.month_name[today.month],
        "goals": engine.today_progress(learner), "goal": engine.goal_for(learner),
        "heat": engine.heatmap(learner), "badges": all_badges, "next_badge": engine.next_badge(all_badges),
        "earned": sum(1 for b in all_badges if b["earned"]),
        "summary": [("week", "This week", "এই সপ্তাহ", _summary(learner, now - timedelta(days=7))),
                    ("month", "This month", "এই মাস", _summary(learner, now - timedelta(days=30))),
                    ("all", "All time", "সব সময়", _summary(learner, None))],
        "mix": engine.practice_mix(learner), "trend": _score_trend(learner),
        "freezes": range(engine.FREEZES_PER_MONTH),
    })


@require_POST
@learner_required
def goals(request):
    goal = engine.goal_for(request.learner)
    try:
        goal.xp = max(10, min(500, int(request.POST.get("xp", goal.xp))))
        goal.questions = max(1, min(200, int(request.POST.get("questions", goal.questions))))
        goal.lessons = max(1, min(10, int(request.POST.get("lessons", goal.lessons))))
        goal.save()
        messages.success(request, "Daily goals saved.")
    except ValueError:
        messages.error(request, "Please use numbers for goals.")
    return redirect("growth:streaks")


# ------------------------------------------------------------------ leaderboard

@learner_required
def leaderboard(request):
    learner = request.learner
    tab = request.GET.get("tab", "league")
    rows, mine, size = engine.league_board(learner)
    family = stats.leaderboard(request.family)
    fam_streaks = sorted(({"learner": l, **engine.streak_info(l)} for l in request.family.learners.all()),
                         key=lambda r: (-r["streak"], -r["best"]))
    return render(request, "growth/leaderboard.html", {
        "tab": tab, "rows": rows, "mine": mine, "size": size, "family": family, "fam_streaks": fam_streaks,
        "league": learner.league, "league_name": engine.LEAGUE_NAME.get(learner.league),
        "league_icon": engine.LEAGUE_ICON.get(learner.league), "leagues": engine.LEAGUES,
        "promote": engine.PROMOTE, "week_end": engine.week_start() + timedelta(days=7),
    })


# ------------------------------------------------------------------ profile and devices

@learner_required
def profile(request):
    learner = request.learner
    if request.method == "POST":
        nick = (request.POST.get("nickname") or "").strip()[:24]
        avatar = request.POST.get("avatar") or learner.avatar
        learner.nickname = "".join(ch for ch in nick if ch.isalnum() or ch in " _-")
        if avatar in Learner.AVATARS:
            learner.avatar = avatar
        learner.save(update_fields=["nickname", "avatar"])
        messages.success(request, "Profile saved.")
        return redirect("growth:profile")
    alive = set(Session.objects.filter(expire_date__gt=timezone.now()).values_list("session_key", flat=True))
    UserDevice.objects.filter(user=request.user).exclude(session_key__in=alive).delete()
    devices = UserDevice.objects.filter(user=request.user)
    all_badges = engine.badges(learner)
    return render(request, "growth/profile.html", {
        "learner": learner, "avatars": Learner.AVATARS, "badges": [b for b in all_badges if b["earned"]],
        "badge_total": len(all_badges), "panel": engine.xp_panel(learner), "devices": devices,
        "current_key": request.session.session_key, "info": engine.streak_info(learner),
    })


@require_POST
@family_required
def signout_others(request):
    keys = list(UserDevice.objects.filter(user=request.user).exclude(session_key=request.session.session_key)
                .values_list("session_key", flat=True))
    Session.objects.filter(session_key__in=keys).delete()
    UserDevice.objects.filter(session_key__in=keys).delete()
    messages.success(request, f"Signed out {len(keys)} other device(s).")
    return redirect("growth:profile")


# ------------------------------------------------------------------ ideas and what's new

@family_required
def ideas(request):
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()[:120]
        details = (request.POST.get("details") or "").strip()[:1000]
        if len(title) < 5:
            messages.error(request, "Please write a short title for your idea.")
        else:
            idea = FeatureIdea.objects.create(family=request.family, user=request.user, title=title, details=details)
            FeatureVote.objects.get_or_create(idea=idea, user=request.user)
            messages.success(request, "Thank you! Other families can now vote for your idea.")
        return redirect("growth:ideas")
    status = request.GET.get("status", "")
    qs = FeatureIdea.objects.annotate(n=Count("votes")).order_by("-n", "-created_at")
    if status in FeatureIdea.Status.values:
        qs = qs.filter(status=status)
    mine = set(FeatureVote.objects.filter(user=request.user).values_list("idea_id", flat=True))
    return render(request, "growth/ideas.html", {"ideas": qs[:100], "mine": mine, "status": status,
                                                 "statuses": FeatureIdea.Status.choices})


@require_POST
@family_required
def vote(request, pk):
    idea = get_object_or_404(FeatureIdea, pk=pk)
    v, created = FeatureVote.objects.get_or_create(idea=idea, user=request.user)
    if not created:
        v.delete()
    return redirect(request.POST.get("next") or "growth:ideas")


def whats_new(request):
    return render(request, "growth/whats_new.html", {"changes": CHANGES})
