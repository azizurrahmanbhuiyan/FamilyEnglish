import calendar
import random
from datetime import date

from django.contrib import messages
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from . import clips, family_talk
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.access import can_open_lesson, locked, paid_required
from core.utils import learner_required

from . import planner, stats, tracks, video
from .forms import PlanForm
from .models import (FamilyTalkSet, Lesson, TalkTopic, VideoClip, Level, PlacementQuestion, PlanDay, Progress, Skill)
from .placement import (READER_MAX, READER_MIN, SPEAKING_CAN_DO, save_placement,
                        score_reader, score_young_child)


def _shuffled(questions):
    """Attach shuffled choices so the right answer is not always in the same place."""
    out = list(questions)
    for q in out:
        q.shuffled = random.sample(q.choice_list(), len(q.choice_list()))
    return out


def _can_open(family, lesson):
    """Phonics lessons are free for everyone; the rest needs the family plan."""
    return can_open_lesson(family, lesson)


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
        week = plan.days.filter(date__gte=t).select_related("lesson", "course_lesson", "topic", "deck")[:6]
    done_ids = set(Progress.objects.filter(learner=learner).values_list("lesson_id", flat=True))

    # "Up next" videos: the next unfinished lessons in the plan, else in the learner's level.
    if mission and plan.kind != "course":
        up_ids = list(plan.days.filter(status=PlanDay.Status.TODO, lesson__isnull=False)
                      .order_by("date").values_list("lesson_id", flat=True)[:4])
    else:
        start = placement.overall if placement else 0
        up_ids = list(Lesson.objects.filter(module__level__number__gte=start).exclude(id__in=done_ids)
                      .values_list("id", flat=True)[:4])
    by_id = {l.id: l for l in _lessons_qs().filter(id__in=up_ids)}
    up_next = [_video_card(by_id[i], done_ids) for i in up_ids if i in by_id]
    featured = up_next.pop(0) if up_next else None

    from course.models import COURSE_SKILLS, SKILL_EMOJI
    from course.path import start_bands, why_text
    from growth import engine, tips

    bands, levels, smart = start_bands(learner)
    measured = smart.finished_at if smart else (placement.taken_at if placement else None)
    skill_levels = [{"skill": s, "emoji": SKILL_EMOJI[s], "level": levels.get(s, 0), "band": bands.get(s, "easy"),
                     "percent": round((levels.get(s) or 0) * 100 / 8)} for s in COURSE_SKILLS]
    strip, strip_on = engine.consistency(learner, 14)
    lang = request.session.get("lang", "en")
    why = ""
    if mission and mission.course_lesson_id:
        why = why_text(mission.course_lesson, learner, lang)
    elif mission and mission.lesson_id:
        why = (f"Level {mission.lesson.module.level.number}: {mission.lesson.module.title}. "
               "Lessons follow the order of your plan.")
    talk_today = _talk_of_the_day(request, learner, mission, placement)
    return render(request, "learning/today.html", {
        "talk_today": talk_today,
        "placement": placement, "smart": smart, "measured": measured, "skill_levels": skill_levels,
        "strip": strip, "strip_on": strip_on, "goals": engine.today_progress(learner),
        "tip": tips.daily_tip(request, learner), "why": why,
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
    if request.method == "POST" and request.POST.get("track") in tracks.TRACKS:
        try:
            dpw = int(request.POST.get("days_per_week", 5))
            mpd = int(request.POST.get("minutes_per_day", 20))
        except ValueError:
            dpw, mpd = 5, 20
        dpw = dpw if dpw in planner.WEEKDAY_SETS else 5
        mpd = mpd if mpd in (15, 20, 30) else 20
        try:
            months = int(request.POST.get("ielts_months") or 0) or None
        except ValueError:
            months = None
        plan = tracks.build_track_plan(learner, request.POST["track"], dpw, mpd, timezone.localdate(),
                                       months=months if request.POST["track"] == "ielts" else None)
        length = f"{plan.months // 12}-year" if plan.months % 12 == 0 else f"{plan.months}-month"
        messages.success(request, f"Your {length} course is ready. "
                                  "New lessons and repeat days are spread over the whole time.")
        return redirect("learning:plan")
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
    rec = tracks.recommend_months(learner)
    track_cards = [dict(key=k, years=v["years"], en=v["en"], bn=v["bn"], why_en=v["why_en"], why_bn=v["why_bn"],
                        months_options=v.get("months_options"), stages=tracks.summary(k, rec))
                   for k, v in tracks.TRACKS.items()]
    return render(request, "learning/plan_new.html", {"form": form, "feas": feas, "placement": placement,
                                                      "track_cards": track_cards,
                                                      "my_track": learner.course_track, "ielts_rec": rec,
                                                      "has_test": learner.smart_tests.filter(
                                                          finished_at__isnull=False).exists()})


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
    for d in plan.days.filter(date__year=year, date__month=month).select_related("lesson", "course_lesson", "topic", "deck"):
        by_date.setdefault(d.date, []).append(d)
    cal = calendar.Calendar(firstweekday=6)  # Sunday first
    weeks = [[(day, by_date.get(day, [])) for day in week] for week in cal.monthdatescalendar(year, month)]
    prev_m = (year, month - 1) if month > 1 else (year - 1, 12)
    next_m = (year, month + 1) if month < 12 else (year + 1, 1)
    done, total = plan.progress()
    return render(request, "learning/plan.html", {
        "focus": planner.week_focus(plan, today),
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
        return locked(request, f"Lesson: {lesson.title}", f"পাঠ: {lesson.title}")
    view = request.GET.get("view") or ("kid" if request.learner.role == "child" else "parent")
    progress = Progress.objects.filter(learner=request.learner, lesson=lesson).first()
    ordered = list(Lesson.objects.filter(module__level=lesson.module.level).order_by(
        "module__order", "order").values_list("id", flat=True))
    idx = ordered.index(lesson.id)
    nxt = ordered[idx + 1] if idx + 1 < len(ordered) else None
    scenes = video.build_scenes(lesson)
    talk, custom = family_talk.talk_for(lesson, request.family, original=request.GET.get("talk") == "original")
    return render(request, "learning/lesson.html", {
        **clips.clip_context(lesson),
        "talk": talk, "talk_custom": custom, "talk_said": family_talk.said_keys(request.learner, lesson),
        "talk_has_custom": lesson.talk_sets.filter(family=request.family).exists(),
        "talk_xp": family_talk.TALK_XP, "ai_on": _ai_enabled(),
        "lesson": lesson, "view": view, "progress": progress,
        "items": lesson.items.all(), "videos": lesson.videos.all(), "next_id": nxt,
        "scenes": scenes, "duration": video.duration_label(round(sum(x["ms"] for x in scenes) / 1000)),
        "thumb": video.thumb_for(lesson),
    })


def _talk_of_the_day(request, learner, mission, placement):
    """One family talk for today: today's level lesson (or the learner's level), a new member each day."""
    lesson = mission.lesson if mission and mission.lesson_id else None
    if lesson is None:
        lv = placement.overall if placement else 0
        lessons = list(Lesson.objects.filter(module__level__number=lv).exclude(family_talk=[]))
        if not lessons:
            return None
        lesson = lessons[timezone.localdate().toordinal() % len(lessons)]
    talk, _ = family_talk.talk_for(lesson, request.family)
    if not talk:
        return None
    card = talk[timezone.localdate().toordinal() % len(talk)]
    return {"lesson": lesson, "card": card, "said": card["key"] in family_talk.said_keys(learner, lesson)}


def _ai_enabled():
    from practice import ai
    return ai.enabled()


def _back_to_talk(request, lesson):
    nxt = request.POST.get("next") or ""
    if nxt.startswith("/") and not nxt.startswith("//"):
        return redirect(nxt)
    return redirect(reverse("learning:lesson", args=[lesson.pk]) + "#talk")


@require_POST
@learner_required
def talk_said(request, pk, who):
    """'We said it together' for one family member: +5 XP once per lesson and member."""
    from growth.engine import award

    lesson = get_object_or_404(Lesson, pk=pk)
    if who in family_talk.MEMBER_KEYS:
        if award(request.learner, family_talk.TALK_XP, "family talk", key=f"talk-{lesson.pk}-{who}"):
            name = family_talk.MEMBER_INFO[who]["name"]
            messages.success(request, f"+{family_talk.TALK_XP} XP — great talking with {name}!")
    return _back_to_talk(request, lesson)


@require_POST
@paid_required("New family talks made by AI", "AI দিয়ে নতুন পারিবারিক কথা")
def talk_ai(request, pk):
    """Ask the AI for a fresh set of 'Talk at home' sentences for this lesson (saved for this family)."""
    from practice import ai

    lesson = get_object_or_404(Lesson.objects.select_related("module__level"), pk=pk)
    if not ai.enabled():
        messages.info(request, "New AI sentences need the AI key (FE_AI_API_KEY). The built-in sentences are ready to use.")
    elif ai.left_today(request.learner) <= 0:
        messages.info(request, "You've used today's AI help. Try again tomorrow.")
    else:
        data = family_talk.ai_generate(lesson, request.learner)
        if data:
            FamilyTalkSet.objects.create(family=request.family, lesson=lesson, learner=request.learner, data=data)
            messages.success(request, "✨ New sentences are ready. Try them with your family!")
        else:
            messages.error(request, "The AI couldn't make new sentences just now. Please try again.")
    return _back_to_talk(request, lesson)


TALK_TABS = [("daily", "🌞", "Daily life", "দৈনন্দিন জীবন"), ("study", "📚", "Topics", "বিষয়"),
             ("trip", "🧳", "Trips", "বেড়ানো"), ("person", "👪", "By family member", "সদস্য অনুযায়ী")]


@paid_required("Talk at home theme lessons", "বাসায় কথা বলার থিম পাঠ")
def talk_hub(request):
    """Talk at home: theme lessons (daily life, topics, trips) and all lesson talks by family member."""
    learner = request.learner
    tab = request.GET.get("tab") or ("person" if request.GET.get("who") else "daily")
    if tab not in [t[0] for t in TALK_TABS]:
        tab = "daily"
    ctx = {"tab": tab, "tabs": TALK_TABS, "members": family_talk.MEMBERS, "talk_xp": family_talk.TALK_XP}
    if tab != "person":
        keys = learner.xp_events.filter(key__startswith="topic-").values_list("key", flat=True)
        done = {}
        for k in keys:
            _, tid, _who = k.split("-", 2)
            done[int(tid)] = done.get(int(tid), 0) + 1
        topics = list(TalkTopic.objects.filter(group=tab))
        for t in topics:
            t.done = done.get(t.pk, 0)
        ctx["topics"] = topics
        return render(request, "learning/talk_hub.html", ctx)
    who = request.GET.get("who", "mamma")
    if who not in family_talk.MEMBER_KEYS:
        who = "mamma"
    placement = learner.placements.first()
    try:
        level = int(request.GET.get("level", placement.overall if placement else 0))
    except ValueError:
        level = 0
    level = max(0, min(8, level))
    lessons = Lesson.objects.filter(module__level__number=level).select_related("module__level")
    rows = []
    for l in lessons:
        talk, _ = family_talk.talk_for(l, request.family)
        card = next((c for c in talk if c["key"] == who), None)
        if card:
            rows.append({"lesson": l, "card": card, "open": _can_open(request.family, l),
                         "said": who in family_talk.said_keys(learner, l)})
    ctx.update(who=who, member=family_talk.MEMBER_INFO[who], level=level, levels=range(0, 9), rows=rows)
    return render(request, "learning/talk_hub.html", ctx)


@paid_required("Talk at home theme lessons", "বাসায় কথা বলার থিম পাঠ")
def talk_topic(request, slug):
    topic = get_object_or_404(TalkTopic, slug=slug)
    talk, custom = family_talk.talk_for(topic, request.family, original=request.GET.get("talk") == "original")
    same = list(TalkTopic.objects.filter(group=topic.group))
    i = same.index(topic)
    return render(request, "learning/talk_topic.html", {
        **clips.clip_context(topic),
        "topic": topic, "talk": talk, "talk_custom": custom,
        "talk_has_custom": topic.talk_sets.filter(family=request.family).exists(),
        "talk_said": family_talk.said_keys(request.learner, topic=topic), "talk_xp": family_talk.TALK_XP,
        "ai_on": _ai_enabled(), "prev": same[i - 1] if i > 0 else None,
        "next": same[i + 1] if i + 1 < len(same) else None,
    })


@require_POST
@paid_required("Talk at home theme lessons", "বাসায় কথা বলার থিম পাঠ")
def topic_said(request, slug, who):
    from growth.engine import award

    topic = get_object_or_404(TalkTopic, slug=slug)
    if who in family_talk.MEMBER_KEYS:
        planner.tick_days(request.learner, topic=topic)
        if award(request.learner, family_talk.TALK_XP, "family talk", key=f"topic-{topic.pk}-{who}"):
            messages.success(request, f"+{family_talk.TALK_XP} XP — great talking with "
                                      f"{family_talk.MEMBER_INFO[who]['name']}!")
    return redirect(reverse("learning:talk_topic", args=[topic.slug]) + "#talk")


@require_POST
@paid_required("Talk at home theme lessons", "বাসায় কথা বলার থিম পাঠ")
def topic_ai(request, slug):
    from practice import ai

    topic = get_object_or_404(TalkTopic, slug=slug)
    if not ai.enabled():
        messages.info(request, "New AI sentences need the AI key (FE_AI_API_KEY). The built-in sentences are ready to use.")
    elif ai.left_today(request.learner) <= 0:
        messages.info(request, "You've used today's AI help. Try again tomorrow.")
    else:
        data = family_talk.ai_generate(None, request.learner, topic=topic)
        if data:
            FamilyTalkSet.objects.create(family=request.family, topic=topic, learner=request.learner, data=data)
            messages.success(request, "✨ New sentences are ready. Try them with your family!")
        else:
            messages.error(request, "The AI couldn't make new sentences just now. Please try again.")
    return redirect(reverse("learning:talk_topic", args=[topic.slug]) + "#talk")


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
    from growth.engine import award

    day = get_object_or_404(PlanDay, pk=pk, plan__learner=request.learner)
    if day.kind in ("review", "family"):
        day.status = PlanDay.Status.DONE
        day.save()
        award(request.learner, day.xp, f"{day.kind} day", key=f"day-{day.pk}")
    nxt = request.POST.get("next") or ""
    return redirect(nxt if nxt.startswith("/") else "learning:plan")


@learner_required
def plan_day(request, pk):
    """One day of the plan: the task, why it is today, XP, the note and video links."""
    from course.path import why_text

    day = get_object_or_404(PlanDay.objects.select_related("lesson__module__level", "course_lesson", "topic", "deck"),
                            pk=pk, plan__learner=request.learner)
    lang = request.session.get("lang", "en")
    if day.deck_id and day.kind != "review":
        why = ("এই সপ্তাহের শব্দ: ব্রিটিশ উচ্চারণে শুনুন, বলুন, বানান করুন আর বাক্যে লিখুন। শেষ করলে শব্দগুলো ফ্ল্যাশকার্ডে ফিরে আসবে।"
               if lang == "bn" else "This week's words: hear them in a British voice, say them, spell them and use "
               "them in sentences. When you finish, they come back as flashcards.")
    elif day.kind == "review" and day.item:
        why = ("আগে শেখা পাঠটি আবার করুন। বারবার করলে শেখা জিনিস মুখে চলে আসে।" if lang == "bn" else
               "Do this earlier lesson again. Repeating is how English moves from the head to the mouth.")
    elif day.topic_id:
        why = ("বাসায় কথা বলার পাঠ: নতুন শব্দ শিখুন, তারপর পরিবারের সবার সাথে ছোট কথাগুলো বলুন।" if lang == "bn" else
               "A talk-at-home lesson: learn the new words, then say the short talks with everyone at home.")
    elif day.course_lesson_id:
        why = why_text(day.course_lesson, request.learner, lang)
    elif day.lesson_id:
        lv = day.lesson.module.level
        why = (f"লেভেল {lv.number} ({lv.name}) — \"{day.lesson.module.title}\" অংশের পরের পাঠ। পরিকল্পনা ধাপে ধাপে এগোয়।"
               if lang == "bn" else f"Level {lv.number} ({lv.name}): the next lesson in \"{day.lesson.module.title}\". "
                                    "Your plan goes step by step.")
    elif day.kind == "review":
        why = ("প্রতি ৬টি পাঠের পরে একটি রিভিউ দিন, যাতে শেখা জিনিস মনে থাকে।" if lang == "bn" else
               "After every 6 lessons there is a review day so that what you learned stays in memory.")
    else:
        why = ("শুক্রবার পরিবারের দিন: সপ্তাহের বাড়ির কাজগুলো সবাই মিলে ইংরেজিতে করুন।" if lang == "bn" else
               "Friday is family day: do the week's home tasks together, in English.")
    item = day.item
    videos = list(VideoClip.objects.for_item(item).visible()) if item and not day.deck_id else []
    open_ = True
    if day.lesson_id:
        open_ = _can_open(request.family, day.lesson)
    elif day.deck_id:
        open_ = request.family.has_full_access or day.deck.slug == "kids3000-w001"
    elif item:
        open_ = request.family.has_full_access
    return render(request, "learning/plan_day.html", {"day": day, "why": why, "videos": videos, "is_open": open_})


@require_POST
@learner_required
def plan_restart(request):
    try:
        planner.restart_plan(request.learner, timezone.localdate())
        messages.success(request, "Your plan now starts today. Finished lessons are kept.")
    except ValueError as exc:
        messages.error(request, str(exc))
    return redirect("learning:plan")


@require_POST
@learner_required
def video_watched(request, pk):
    from growth.engine import award

    lesson = get_object_or_404(Lesson, pk=pk)
    if award(request.learner, 5, "video", key=f"video-{lesson.pk}"):
        messages.success(request, "+5 XP for watching. Now try the practice!")
    return redirect(reverse("learning:lesson", args=[lesson.pk]) + "#practice")


# ---------- The Phonics Year (36 weeks) ----------

def _year_modules():
    from .models import Module
    mods = (Module.objects.filter(level__number__lte=2).exclude(plan={})
            .select_related("level").prefetch_related("lessons"))
    return sorted(mods, key=lambda m: m.plan["week"])


@learner_required
def phonics_year(request):
    """All 36 weeks by term, the learner's ticks, and the family's check results."""
    mods = _year_modules()
    done = {p.lesson_id: p for p in Progress.objects.filter(learner=request.learner, lesson__module__in=mods)}
    terms = {1: [], 2: [], 3: []}
    checks = []
    for m in mods:
        days = []
        for l in m.lessons.all():
            days.append({"lesson": l, "done": done.get(l.pk), "open": can_open_lesson(request.family, l)})
            if (l.teacher or {}).get("kind") in ("assess1", "assess2"):
                checks.append(l)
        terms[m.plan["term"]].append({"m": m, "days": days, "n_done": sum(1 for d in days if d["done"])})
    learners = list(request.family.learners.all())
    scores = {(p.learner_id, p.lesson_id): p.score for p in Progress.objects.filter(learner__in=learners, lesson__in=checks)}
    table = [{"learner": ln, "cells": [scores.get((ln.pk, c.pk)) for c in checks]} for ln in learners]
    total = sum(len(t) for t in terms.values()) * 5
    return render(request, "learning/phonics_year.html", {
        "terms": [(1, "Term 1 · Sounds and blending", "১ম টার্ম · ধ্বনি ও জোড়া দেওয়া", terms[1]),
                  (2, "Term 2 · Magic e and other spellings", "২য় টার্ম · ম্যাজিক e ও অন্য বানান", terms[2]),
                  (3, "Term 3 · More spellings, stories and the year check", "৩য় টার্ম · আরও বানান, গল্প ও বছর শেষের মূল্যায়ন", terms[3])],
        "checks": checks, "table": table, "done": len(done), "total": total})


@learner_required
def phonics_week(request, n):
    """One week for the teacher: goal, what to prepare, every day's steps, texts and checks. Printable."""
    mods = [m for m in _year_modules() if m.plan["week"] == n]
    if not mods:
        raise Http404
    m = mods[0]
    lessons = list(m.lessons.all())
    if not all(can_open_lesson(request.family, l) for l in lessons):
        return locked(request, f"Phonics Year week {n}", f"ফনিক্স বছর সপ্তাহ {n}")
    return render(request, "learning/phonics_week.html", {
        "m": m, "lessons": [(l, list(l.items.all())) for l in lessons], "n": n,
        "prev": n - 1 if n > 1 else None, "next": n + 1 if n < 36 else None})
