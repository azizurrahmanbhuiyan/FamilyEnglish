"""Talk pages on the website: setup, home, daily talk, role-plays, Read and talk, the chat and the report."""

import json

from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from core.access import locked
from core.utils import learner_required
from practice import ai
from studio.models import Bookmark

from . import engine as TE
from .content import roleplays as RP
from .content import topics as T
from .models import TalkSession


def _settings(prof):
    rate = dict((v, v) for v, _ in T.SPEEDS).get(prof.speed, 1.0)
    pitch = {k: p for k, *_, p in T.VOICES}.get(prof.voice, 1.0)
    return {"rate": rate, "pitch": pitch}


# ------------------------------------------------------------------ setup questions

@learner_required
def setup(request):
    prof = TE.profile(request.learner)
    if request.method == "POST":
        data = {k: request.POST.get(k) for k in ("level", "reason", "challenge", "correct", "voice", "speed", "daily_minutes")}
        data["interests"] = request.POST.getlist("interests")
        TE.save_profile(prof, data)
        return redirect("talk:home")
    return render(request, "talk/setup.html", {
        "p": prof, "levels": T.LEVELS, "reasons": T.REASONS, "challenges": T.CHALLENGES, "corrects": T.CORRECT,
        "voices": T.VOICES, "speeds": T.SPEEDS, "goals": T.DAILY_GOALS, "interests": T.INTERESTS})


# ------------------------------------------------------------------ home

@learner_required
def home(request):
    learner = request.learner
    prof = TE.profile(learner)
    if not prof.done:
        return redirect("talk:setup")
    cat, q = TE.daily_topic(learner, prof)
    paid = request.family.has_full_access
    recent = TalkSession.objects.filter(learner=learner).exclude(report=None)[:6]
    return render(request, "talk/home.html", {
        "p": prof, "cat": cat, "question": q, "paid": paid, "daily_ok": TE.can_open(request.family, learner, "daily"),
        "minutes": TE.minutes_today(learner), "goal": prof.daily_minutes, "recent": recent,
        "for_you": RP.for_you(prof.reason, 4), "free": RP.FREE, "ai_on": ai.enabled(),
        "articles": [T.BY_KEY[k]["seed"] | {"emoji": T.BY_KEY[k]["emoji"]} for k in (prof.interests or ["travel", "food"])[:3] if k in T.BY_KEY]})


# ------------------------------------------------------------------ starting talks

@require_POST
@learner_required
def go(request, kind, ref=""):
    if kind not in ("daily", "roleplay", "article", "custom"):
        raise Http404
    if not TE.can_open(request.family, request.learner, kind, ref):
        return locked(request, "Talk lessons", "কথা বলার পাঠ")
    s = TE.start(request.learner, kind, ref, request.POST.get("setting", ""), request.POST.get("persona", ""))
    if not s:
        raise Http404
    return redirect("talk:chat", pk=s.pk)


@learner_required
def roleplays(request):
    prof = TE.profile(request.learner)
    tab = request.GET.get("t", "foryou")
    cat = request.GET.get("c", "")
    if tab == "popular":
        items = [RP.BY_SLUG[s] for s in RP.POPULAR]
    elif cat:
        items = [r for r in RP.ROLEPLAYS if r["category"] == cat]
    else:
        items = RP.for_you(prof.reason, 40)
    return render(request, "talk/roleplays.html", {"items": items, "tab": tab, "cat": cat, "categories": RP.CATEGORIES,
                                                   "paid": request.family.has_full_access, "free": RP.FREE, "ai_on": ai.enabled()})


@learner_required
def read(request):
    prof = TE.profile(request.learner)
    lib = TE.library(request.family.has_full_access)
    mine = [c for c in lib if c["key"] in prof.interests]
    rest = [c for c in lib if c["key"] not in prof.interests]
    return render(request, "talk/read.html", {"sections": mine + rest, "mine": {c["key"] for c in mine}, "ai_on": ai.enabled()})


@learner_required
def article(request, slug):
    if not TE.can_open(request.family, request.learner, "article", slug):
        return locked(request, "Read and talk", "পড়ুন ও বলুন")
    a = TE.article(slug)
    if not a:
        raise Http404
    cat = T.BY_KEY.get(a["category"])
    return render(request, "talk/article.html", {"a": a, "cat": cat, "paras": a["body"].split("\n\n"),
                                                 "tts": _settings(TE.profile(request.learner))})


# ------------------------------------------------------------------ the chat and the report

def _mine(request, pk):
    return get_object_or_404(TalkSession, pk=pk, learner=request.learner)


@learner_required
def chat(request, pk):
    s = _mine(request, pk)
    if s.report:
        return redirect("talk:report", pk=s.pk)
    prof = TE.profile(request.learner)
    cfg = {"id": s.pk, "messages": s.messages, "maxTurns": TE.MAX_TURNS, "aiOn": TE.ai_ok(request.learner),
           "urls": {k: reverse(f"talk:api_{k}", args=[s.pk]) for k in ("reply", "hint", "translate", "finish")},
           "report": reverse("talk:report", args=[s.pk]), **_settings(prof)}
    return render(request, "talk/chat.html", {"s": s, "cfg": cfg})


@learner_required
def report(request, pk):
    s = _mine(request, pk)
    r = TE.finish(request.learner, s)
    saved = set(Bookmark.objects.filter(learner=request.learner).values_list("text", flat=True))
    cfg = {"practice": reverse("talk:api_practice", args=[s.pk]), "bookmark": reverse("studio:api_bookmark"), "saved": list(saved),
           **_settings(TE.profile(request.learner))}
    return render(request, "talk/report.html", {"s": s, "r": r, "cfg": cfg, "again": _again(s)})


def _again(s):
    if s.kind == "roleplay":
        return reverse("talk:go_ref", args=["roleplay", s.ref])
    if s.kind == "article":
        return reverse("talk:go_ref", args=["article", s.ref])
    return ""


# ------------------------------------------------------------------ JSON for talk.js

def _json_view(view):
    from functools import wraps

    @wraps(view)
    @learner_required
    @require_POST
    def inner(request, pk):
        try:
            d = json.loads(request.body or "{}")
        except ValueError:
            d = {}
        return view(request, _mine(request, pk), d)
    return inner


@_json_view
def api_reply(request, s, d):
    if s.report:
        return JsonResponse({"reply": "", "done": True})
    return JsonResponse(TE.reply(request.learner, s, d.get("text", ""), d.get("confidence"), d.get("seconds", 0)))


@_json_view
def api_hint(request, s, d):
    return JsonResponse({"hint": TE.hint(request.learner, s)})


@_json_view
def api_translate(request, s, d):
    return JsonResponse({"text": TE.translate(request.learner, s, d.get("text", ""))})


@_json_view
def api_finish(request, s, d):
    TE.finish(request.learner, s)
    return JsonResponse({"ok": True, "url": reverse("talk:report", args=[s.pk])})


@_json_view
def api_practice(request, s, d):
    target = (d.get("target") or "")[:300]
    if not target:
        return JsonResponse({"ok": False}, status=400)
    res = TE.practice_score(target, d.get("said", ""), d.get("confidence"))
    from studio import engine as E
    E.record(request.learner, "repeat", f"talk:{s.pk}:better", target, d.get("said", ""), res["score"])
    return JsonResponse(res)
