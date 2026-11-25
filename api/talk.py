"""Talk for the phone app: the same lessons, reports and rules as the website (talk.engine)."""

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from practice import ai
from talk import engine as TE
from talk.content import roleplays as RP
from talk.content import topics as T
from talk.models import TalkSession

from .auth import learner_of
from .views import _locked


def _opts():
    return {"levels": [{"n": n, "en": en, "bn": bn, "desc": d} for n, en, bn, d in T.LEVELS],
            "reasons": [{"key": k, "emoji": e, "en": en, "bn": bn} for k, e, en, bn in T.REASONS],
            "challenges": [{"key": k, "emoji": e, "en": en, "bn": bn} for k, e, en, bn in T.CHALLENGES],
            "correct": [{"key": k, "en": en, "bn": bn} for k, en, bn in T.CORRECT],
            "voices": [{"key": k, "en": en, "bn": bn, "pitch": p} for k, en, bn, p in T.VOICES],
            "speeds": [{"value": v, "label": lab} for v, lab in T.SPEEDS],
            "goals": T.DAILY_GOALS,
            "interests": [{"key": k, "emoji": e, "en": en, "bn": bn} for k, e, en, bn in T.INTERESTS]}


def _rp(r, paid):
    return {"slug": r["slug"], "icon": r["icon"], "category": r["category"], "title": r["title"], "title_bn": r["title_bn"],
            "goal": r["goal"], "locked": not paid and r["slug"] not in RP.FREE}


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def profile(request):
    learner = learner_of(request)
    p = TE.profile(learner)
    if request.method == "POST":
        TE.save_profile(p, request.data)
    return Response({"profile": TE.profile_json(p), "options": _opts()})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def home(request):
    learner = learner_of(request)
    p = TE.profile(learner)
    cat, q = TE.daily_topic(learner, p)
    paid = request.family.has_full_access
    recent = TalkSession.objects.filter(learner=learner).exclude(report=None)[:6]
    return Response({"setup_done": p.done, "daily": {"category": cat["key"], "emoji": cat["emoji"], "title": cat["title"],
                                                     "title_bn": cat["title_bn"], "question": q,
                                                     "ok": TE.can_open(request.family, learner, "daily")},
                     "minutes": TE.minutes_today(learner), "goal": p.daily_minutes, "ai": ai.enabled(), "paid": paid,
                     "speed": p.speed, "pitch": {k: pi for k, *_, pi in T.VOICES}.get(p.voice, 1.0),
                     "for_you": [_rp(r, paid) for r in RP.for_you(p.reason, 4)],
                     "recent": [{"id": s.pk, "title": s.title, "score": (s.report or {}).get("score", 0),
                                 "date": s.created_at.strftime("%d %b")} for s in recent]})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def roleplays(request):
    learner = learner_of(request)
    p = TE.profile(learner)
    paid = request.family.has_full_access
    return Response({"for_you": [_rp(r, paid) for r in RP.for_you(p.reason, 8)],
                     "popular": [_rp(RP.BY_SLUG[s], paid) for s in RP.POPULAR],
                     "categories": [{"key": k, "en": en, "bn": bn, "items": [_rp(r, paid) for r in RP.ROLEPLAYS if r["category"] == k]}
                                    for k, en, bn in RP.CATEGORIES],
                     "custom_ok": paid and ai.enabled()})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def library(request):
    learner_of(request)
    return Response({"sections": [{**c, "items": [i for i in c["items"] if i["ready"]]} for c in TE.library(request.family.has_full_access)]})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def article(request, slug):
    learner = learner_of(request)
    if not TE.can_open(request.family, learner, "article", slug):
        return _locked()
    a = TE.article(slug)
    if not a:
        return Response({"detail": "Article not found."}, status=404)
    return Response(a)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start(request):
    learner = learner_of(request)
    kind, ref = request.data.get("kind", ""), request.data.get("ref", "") or ""
    if not TE.can_open(request.family, learner, kind, ref):
        return _locked()
    s = TE.start(learner, kind, ref, request.data.get("setting", "") or "", request.data.get("persona", "") or "")
    if not s:
        return Response({"detail": "That talk does not exist."}, status=404)
    return Response(TE.session_json(s))


def _session(request, pk):
    learner = learner_of(request)
    return learner, get_object_or_404(TalkSession, pk=pk, learner=learner)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reply(request, pk):
    learner, s = _session(request, pk)
    if s.report:
        return Response({"reply": "", "tip": "", "done": True})
    return Response(TE.reply(learner, s, request.data.get("text", ""), request.data.get("confidence"), request.data.get("seconds", 0)))


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def hint(request, pk):
    learner, s = _session(request, pk)
    return Response({"hint": TE.hint(learner, s)})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def translate(request, pk):
    learner, s = _session(request, pk)
    return Response({"text": TE.translate(learner, s, request.data.get("text", ""))})


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def finish(request, pk):
    learner, s = _session(request, pk)
    return Response({"title": s.title, "report": TE.finish(learner, s)})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def practice(request, pk):
    from studio import engine as E
    learner, s = _session(request, pk)
    target = (request.data.get("target") or "")[:300]
    if not target:
        return Response({"detail": "Nothing to practise."}, status=400)
    res = TE.practice_score(target, request.data.get("said", ""), request.data.get("confidence"))
    E.record(learner, "repeat", f"talk:{s.pk}:better", target, request.data.get("said", ""), res["score"])
    return Response(res)
