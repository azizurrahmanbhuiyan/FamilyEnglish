"""FamilyEnglish API, version 1 — the same data the website uses, as JSON for the phone app.

Everything here reuses the website's own code (studio.engine, studio.shorts, studio.content),
so the app and the website always agree on scores, XP, gems and what is free.
"""

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from studio import engine as E
from studio import shorts as SH
from studio.content import grammar as G
from studio.content import sounds as S
from studio.content import units as U
from studio.models import LessonDone

from .auth import family_of, learner_of


class LoginThrottle(AnonRateThrottle):
    rate = "10/min"


def _locked():
    return Response({"locked": True, "detail": "This part is in the family plan."}, status=status.HTTP_402_PAYMENT_REQUIRED)


# ------------------------------------------------------------------ sign in

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([LoginThrottle])
def login(request):
    """POST {email, password} -> {token, family, learners}."""
    email = (request.data.get("email") or "").strip().lower()
    user = authenticate(request, username=email, password=request.data.get("password") or "")
    if not user:
        return Response({"detail": "Email or password is not right."}, status=status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)
    request.user = user
    family = family_of(request)
    return Response({"token": token.key, "family": _family(family), "learners": _learners(family)})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return Response({"ok": True})


def _family(family):
    return {"name": family.name, "paid": family.has_full_access,
            "paid_until": family.paid_until.isoformat() if family.paid_until else None}


def _learners(family):
    return [{"id": l.id, "name": l.name, "avatar": l.avatar, "role": l.role, "track": l.track} for l in family.learners.all()]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    family = family_of(request)
    return Response({"family": _family(family), "learners": _learners(family)})


# ------------------------------------------------------------------ Today

def _bar(learner):
    from growth import engine as growth
    info = growth.streak_info(learner)
    return {"streak": info["streak"], "active_today": info["active_today"], "gems": E.wallet(learner).gems,
            "xp": growth.totals(learner)["xp"]}


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def today(request):
    learner = learner_of(request)
    sc = E.scores(learner)
    done = E.done_keys(learner)
    unit = E.current_unit(learner, done)
    tasks = [{"label": t["label"], "label_bn": t["label_bn"], "lesson": t["n"], "done": t["done"],
              "unit": t["unit"]["slug"], "unit_title": t["unit"]["title"], "emoji": t["unit"]["emoji"]}
             for t in E.today_tasks(learner)]
    from studio.views import _word_of_day
    w = _word_of_day()
    return Response({
        "learner": {"id": learner.id, "name": learner.name, "avatar": learner.avatar},
        "bar": _bar(learner), "journey": E.journey(learner, sc), "ielts": sc["ielts"], "tasks": tasks,
        "week": [{"day": d["day"].isoformat(), "label": d["label"], "on": d["on"], "today": d["today"]} for d in E.streak_week(learner)],
        "continue": {"unit": unit["slug"], "title": unit["title"], "emoji": unit["emoji"], **E.unit_progress(unit, done)},
        "word_of_day": {"word": w.word, "ipa": w.ipa, "definition": w.definition, "bn": w.meaning_bn} if w else None,
        "shorts_today": SH.done_today(learner),
    })


# ------------------------------------------------------------------ Learn: units and lessons

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def units(request):
    learner = learner_of(request)
    done = E.done_keys(learner)
    paid = request.family.has_full_access
    return Response([{"slug": u["slug"], "number": i, "emoji": u["emoji"], "level": u["level"], "title": u["title"],
                      "title_bn": u["title_bn"], "free": u["slug"] in U.FREE, "locked": not (paid or u["slug"] in U.FREE),
                      **E.unit_progress(u, done)} for i, u in enumerate(U.UNITS, 1)])


def _word_item(entry):
    from studio.views import _ipa_lookup
    p = U.parse_word(entry)
    tip_en, tip_bn = S.tip(p["sound"])
    return {"text": p["text"], "before": p["before"], "target": p["target"], "after": p["after"], "sound": p["sound"],
            "bn": p["bn"], "ipa": _ipa_lookup([p["text"]]).get(p["text"].lower(), ""), "tip_en": tip_en, "tip_bn": tip_bn}


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unit_detail(request, slug):
    learner = learner_of(request)
    u = U.BY_SLUG.get(slug)
    if not u:
        return Response({"detail": "No such unit."}, status=404)
    done = E.done_keys(learner)
    locked = not (request.family.has_full_access or slug in U.FREE)
    data = {"slug": slug, "emoji": u["emoji"], "title": u["title"], "title_bn": u["title_bn"], "desc": u["desc"],
            "desc_bn": u["desc_bn"], "outcome": u["outcome"], "outcome_bn": u["outcome_bn"], "grammar": u["grammar"],
            "locked": locked, **E.unit_progress(u, done),
            "lessons": [{"n": n, "kind": kind, "title": t, "title_bn": tbn, "difficulty": diff,
                         "done": E.unit_key(slug, n) in done} for n, kind, t, tbn, _, diff in U.LESSON_TYPES]}
    if not locked:
        data["words"] = [_word_item(w) for w in u["words"]]
        data["phrases"] = [{"text": t, "sound": s, "bn": bn, "tip_en": S.tip(s)[0], "tip_bn": S.tip(s)[1]} for t, s, bn in u["phrases"]]
        data["conversation"] = [{"coach": b, "reply": r, "hint": h} for b, r, h in u["convo"]]
        data["speak_prompt"] = u["speak"]
        data["speak_seconds"], data["speak_min_words"] = 60, 45
        data["grammar_lesson"] = _grammar_json(G.BY_SLUG[u["grammar"]])
    return Response(data)


def _grammar_json(g):
    """A grammar lesson for the app: rule, examples and practice (fill / fix / say / make)."""
    practice = []
    for p in g["practice"]:
        if p[0] in ("fill", "fix"):
            practice.append({"type": p[0], "prompt": p[1], "accepted": list(p[2])})
        elif p[0] == "say":
            practice.append({"type": "say", "prompt": p[1]})
        else:
            practice.append({"type": "make", "prompt": p[1], "pattern": p[2]})
    return {"slug": g["slug"], "key": E.grammar_key(g["slug"]), "title": g["title"], "title_bn": g["title_bn"],
            "hello": g["hello"], "formula": [t for t, _ in g["formula"]], "rule": g["rule"],
            "examples": [{"en": en, "bn": bn} for en, bn in g["examples"]], "practice": practice}


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def analyse(request):
    """POST {key, prompt, transcript, seconds} -> speaking feedback (words, wpm, overall, tips). Used by 'Speak freely'."""
    learner = learner_of(request)
    d = request.data
    key = str(d.get("key", ""))[:80]
    if key.startswith("unit:") and not (request.family.has_full_access or key.split(":")[1] in U.FREE):
        return _locked()
    try:
        seconds = max(1, int(float(d.get("seconds") or 0)))
    except (TypeError, ValueError):
        seconds = 1
    transcript = str(d.get("transcript", ""))[:3000]
    res = E.analyse_speech(transcript, seconds, int(d.get("targetWpm") or 110), int(d.get("minWords") or 45))
    res["tips"] = [{"en": en, "bn": bn} for en, bn in res["tips"]]
    E.record(learner, "speech", key or "speech", str(d.get("prompt", ""))[:200], transcript, res["overall"], res["seconds"], res["wpm"])
    return Response(res)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def grammar_list(request):
    learner = learner_of(request)
    done = E.done_keys(learner)
    return Response([{"slug": g["slug"], "level": g["level"], "icon": g["icon"], "title": g["title"], "title_bn": g["title_bn"],
                      "sub": g["sub"], "done": E.grammar_key(g["slug"]) in done,
                      "locked": not (request.family.has_full_access or g["slug"] in G.FREE)} for g in G.LESSONS])


# ------------------------------------------------------------------ practice: tries and finished lessons

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def attempt(request):
    """POST {key, target, said, confidence?, seconds?, kind?} -> {score, marks}. The server scores the try."""
    learner = learner_of(request)
    d = request.data
    target, said = d.get("target", ""), d.get("said", "")
    key = str(d.get("key", ""))[:80]
    if key.startswith("unit:") and not (request.family.has_full_access or key.split(":")[1] in U.FREE):
        return _locked()
    kind = d.get("kind", "repeat") if d.get("kind") in ("repeat", "convo", "words") else "repeat"
    score = E.speech_score(target, said, d.get("confidence")) if said else 0
    E.record(learner, kind, key, target, said, score, d.get("seconds", 0))
    return Response({"score": score, "marks": E.word_marks(target, said) if said and target else []})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def finish(request):
    """POST {key, title, score} -> {first, xp, gems}. XP and gems only the first time."""
    learner = learner_of(request)
    key = str(request.data.get("key", ""))[:80]
    if not key:
        return Response({"detail": "key is needed"}, status=400)
    if key.startswith("unit:") and not (request.family.has_full_access or key.split(":")[1] in U.FREE):
        return _locked()
    score = max(0, min(100, int(request.data.get("score") or 0)))
    done, first = E.finish(learner, key, request.data.get("title", ""), score)
    return Response({"first": first, "score": done.score, "xp": 20 + score // 5 if first else 0,
                     "gems_earned": (5 if score >= 90 else 2) if first else 0, "bar": _bar(learner)})


# ------------------------------------------------------------------ short videos

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def shorts(request):
    learner = learner_of(request)
    try:
        offset = max(0, int(request.query_params.get("offset", 0)))
    except ValueError:
        offset = 0
    items, more, total = SH.feed(learner, request.query_params.get("topic", "all"), offset)
    return Response({"items": items, "more": more, "next": offset + SH.PAGE, "total": total,
                     "topics": [{"key": k, "en": en, "bn": bn, "emoji": em} for k, en, bn, em in SH.TOPICS],
                     "today": SH.done_today(learner), "free_per_day": None if request.family.has_full_access else SH.FREE_PER_DAY})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def short_try(request):
    learner = learner_of(request)
    from growth import engine as growth
    from studio.models import Attempt
    s = SH.by_id(str(request.data.get("id", "")))
    if not s:
        return Response({"detail": "No such short."}, status=404)
    key = f"short:{s['id']}"
    if not request.family.has_full_access:
        tried = Attempt.objects.filter(learner=learner, kind="short", key=key, created_at__date=timezone.localdate()).exists()
        if not tried and SH.done_today(learner) >= SH.FREE_PER_DAY:
            return _locked()
    said = request.data.get("said", "")
    score = E.speech_score(s["line"], said, request.data.get("confidence")) if said else 0
    E.record(learner, "short", key, s["line"], said, score, request.data.get("seconds", 5))
    xp = 5 if score >= 70 and growth.award(learner, 5, "Short video", key=f"{key}:{timezone.localdate():%Y%m%d}"[:80]) else 0
    return Response({"score": score, "marks": E.word_marks(s["line"], said) if said else [], "xp": xp, "today": SH.done_today(learner)})


# ------------------------------------------------------------------ progress and dictionary

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def progress(request):
    learner = learner_of(request)
    sc = E.scores(learner)
    secs = E.learning_seconds(learner)
    badges = E.all_badges(learner)
    return Response({
        "scores": sc, "journey": E.journey(learner, sc), "bar": _bar(learner),
        "learning_minutes": secs // 60, "lessons": E.lessons_count(learner),
        "week": [{"day": d["day"].isoformat(), "label": d["label"], "xp": d["xp"], "minutes": d["minutes"]} for d in E.week(learner)],
        "history": [{"title": h.title or h.key, "score": h.score, "date": h.finished_at.date().isoformat()}
                    for h in LessonDone.objects.filter(learner=learner)[:20]],
        "badges": [{"icon": b["icon"], "name": b["name"], "name_bn": b["name_bn"], "earned": b["earned"], "percent": b["percent"]} for b in badges],
        "certificates": [{"title": c.title, "number": c.number, "date": c.issued_at.date().isoformat()} for c in learner.certificates.all()],
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dictionary(request):
    from practice.models import VocabWord
    learner_of(request)
    q = (request.query_params.get("q") or "").strip()[:60]
    if not q:
        return Response([])
    qs = VocabWord.objects.filter(word__iexact=q).order_by("rank")[:3] or VocabWord.objects.filter(word__istartswith=q).order_by("rank")[:12]
    seen, out = set(), []
    for w in qs:
        if w.word.lower() in seen:
            continue
        seen.add(w.word.lower())
        out.append({"word": w.word, "ipa": w.ipa, "pos": w.pos, "definition": w.definition, "example": w.example, "bn": w.meaning_bn})
    return Response(out)
