"""The five tabs — Today, Learn, Coach, Discover, Progress — and the speaking player behind them."""

import json
import random

from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.access import locked, paid_required
from core.utils import learner_required

from . import engine as E
from .content import coaches as C
from .content import grammar as G
from .content import ielts as I
from .content import pronunciation as PR
from .content import sounds as S
from .content import stories as ST
from .content import units as U
from .models import Attempt, Bookmark, Certificate, LessonDone

ROLE_COLORS = {"subj": "c-subj", "verb": "c-verb", "aux": "c-aux", "obj": "c-obj"}


def _lang(request):
    return request.session.get("lang", "en")


def _ipa_lookup(texts):
    from practice.models import VocabWord
    wanted = {t.lower() for t in texts if " " not in t}
    out = {}
    for w, ipa in VocabWord.objects.filter(word__in=wanted).exclude(ipa="").values_list("word", "ipa"):
        out.setdefault(w.lower(), ipa)
    return out


def _repeat_item(text, before="", target="", after="", sound="", bn="", ipa=""):
    tip_en, tip_bn = S.tip(sound) if sound else S.tip("stress")
    return {"type": "repeat", "text": text, "before": before or text if not target else before, "target": target,
            "after": after, "sound": sound, "bn": bn, "ipa": ipa, "tip_en": tip_en, "tip_bn": tip_bn}


def _word_items(entries):
    parsed = [U.parse_word(e) for e in entries]
    ipas = _ipa_lookup([p["text"] for p in parsed])
    return [_repeat_item(p["text"], p["before"], p["target"], p["after"], p["sound"], p["bn"], ipas.get(p["text"].lower(), ""))
            for p in parsed]


def _phrase_items(phrases):
    return [_repeat_item(text, sound=sound, bn=bn) for text, sound, bn in phrases]


def _sentence_items(sentences, sound=""):
    return [_repeat_item(s, sound=sound) for s in sentences]


def _player(request, *, key, title, title_bn, mode, items=None, back, extra=None, free=False):
    """Render the one speaking player used by every lesson type."""
    learner = request.learner
    best = LessonDone.objects.filter(learner=learner, key=key).values_list("score", flat=True).first()
    config = {"key": key, "mode": mode, "title": title, "items": items or [], "lang": _lang(request),
              "attemptUrl": reverse("studio:api_attempt"), "finishUrl": reverse("studio:api_finish"),
              "bookmarkUrl": reverse("studio:api_bookmark"), "checkUrl": reverse("studio:api_check"),
              "analyseUrl": reverse("studio:api_analyse"), "replyUrl": reverse("studio:api_reply"), "back": back}
    if extra:
        config.update(extra)
    from world.content import localize_player
    localize_player(config, request)
    return render(request, "studio/player.html", {"config": config, "title": title, "title_bn": title_bn,
                                                   "mode": mode, "back": back, "best": best})


# ------------------------------------------------------------------ Today

@learner_required
def today(request):
    learner = request.learner
    sc = E.scores(learner)
    done = E.done_keys(learner)
    unit = E.current_unit(learner, done)
    from learning import planner

    plan, mission = planner.today_mission(learner, timezone.localdate())
    return render(request, "studio/today.html", {
        "tasks": E.today_tasks(learner), "journey": E.journey(learner, sc), "scores": sc,
        "streak_week": E.streak_week(learner), "unit": unit, "unit_progress": E.unit_progress(unit, done),
        "next_lesson": E.next_unit_lesson(unit, done), "plan": plan, "mission": mission,
        "word_of_day": _word_of_day(), "coach_pick": _coach_of_day(), "paid": request.family.has_full_access,
        "free_units": U.FREE,
    })


def _word_of_day():
    from practice.models import VocabWord
    qs = VocabWord.objects.exclude(definition="").exclude(ipa="")
    n = qs.count()
    if not n:
        return None
    day = timezone.localdate().toordinal()
    return qs.order_by("id")[day % n]


def _coach_of_day():
    talk = [c for c in C.COACHES if c["scenarios"]]
    return talk[timezone.localdate().toordinal() % len(talk)]


# ------------------------------------------------------------------ Learn

@learner_required
def learn(request):
    done = E.done_keys(request.learner)
    units = [{**u, "num": i, "progress": E.unit_progress(u, done), "words_parsed": [U.parse_word(w) for w in u["words"]],
              "grammar_lesson": G.BY_SLUG[u["grammar"]], "free": u["slug"] in U.FREE} for i, u in enumerate(U.UNITS, 1)]
    levels = [(lvl, [u for u in units if u["level"] == lvl]) for lvl in ("A1", "A2", "B1")]
    return render(request, "studio/learn.html", {
        "levels": levels, "paid": request.family.has_full_access,
        "grammar_done": sum(1 for k in done if k.startswith("grammar:")), "grammar_total": len(G.LESSONS),
        "pron_done": sum(1 for p in PR.LESSONS if PR.key(p["slug"]) in done), "pron_total": len(PR.LESSONS),
        "stories_total": len(ST.STORIES),
        "ielts_bands": I.BANDS,
    })


@learner_required
def unit(request, slug):
    u = U.BY_SLUG.get(slug) or _404()
    done = E.done_keys(request.learner)
    nxt = E.next_unit_lesson(u, done)
    lessons = [{"n": n, "kind": kind, "title": t, "title_bn": tbn, "icon": icon, "difficulty": diff,
                "done": E.unit_key(slug, n) in done, "next": nxt and nxt[0] == n,
                "score": LessonDone.objects.filter(learner=request.learner, key=E.unit_key(slug, n)).values_list("score", flat=True).first()}
               for n, kind, t, tbn, icon, diff in U.LESSON_TYPES]
    return render(request, "studio/unit.html", {"unit": u, "num": U.UNITS.index(u) + 1, "lessons": lessons, "progress": E.unit_progress(u, done),
                                                "grammar": G.BY_SLUG[u["grammar"]],
                                                "words": [U.parse_word(w) for w in u["words"]],
                                                "locked": not (request.family.has_full_access or slug in U.FREE)})


@learner_required
def unit_lesson(request, slug, n):
    u = U.BY_SLUG.get(slug) or _404()
    if not (request.family.has_full_access or slug in U.FREE):
        return locked(request, "Learn units", "শেখার ইউনিট")
    lt = next((t for t in U.LESSON_TYPES if t[0] == n), None) or _404()
    _, kind, t, tbn, _, _ = lt
    key = E.unit_key(slug, n)
    back = reverse("studio:unit", args=[slug])
    title, title_bn = f"{u['title']} · {t}", f"{u['title_bn']} · {tbn}"
    if kind == "words":
        return _player(request, key=key, title=title, title_bn=title_bn, mode="repeat", items=_word_items(u["words"]), back=back)
    if kind == "sounds":
        return _player(request, key=key, title=title, title_bn=title_bn, mode="repeat", items=_phrase_items(u["phrases"]), back=back)
    if kind == "grammar":
        return redirect(f"{reverse('studio:grammar_lesson', args=[u['grammar']])}?unit={slug}")
    if kind == "convo":
        lines = [{"bot": b, "reply": r, "hint": h} for b, r, h in u["convo"]]
        return _player(request, key=key, title=title, title_bn=title_bn, mode="convo", back=back,
                       extra={"lines": lines, "setting": u["desc"]})
    return _player(request, key=key, title=title, title_bn=title_bn, mode="speak", back=back,
                   extra={"prompt": u["speak"], "seconds": 60, "minWords": 45, "targetWpm": 110})


# ------------------------------------------------------------------ Grammar coach

@learner_required
def grammar(request):
    done = E.done_keys(request.learner)
    level = request.GET.get("level", "A1")
    if level not in [lv[0] for lv in G.LEVELS]:
        level = "A1"
    lessons = [{**g, "done": E.grammar_key(g["slug"]) in done} for g in G.by_level(level)]
    level_info = next(lv for lv in G.LEVELS if lv[0] == level)
    counts = {lv[0]: E.level_done(lv[0], done) for lv in G.LEVELS}
    return render(request, "studio/grammar.html", {"levels": G.LEVELS, "level": level, "level_info": level_info,
                                                   "lessons": lessons, "counts": counts, "paid": request.family.has_full_access,
                                                   "free": G.FREE})


@learner_required
def grammar_lesson(request, slug):
    g = G.BY_SLUG.get(slug) or _404()
    if not (request.family.has_full_access or slug in G.FREE):
        return locked(request, "Grammar coach", "ব্যাকরণ কোচ")
    unit_slug = request.GET.get("unit")
    back = reverse("studio:unit", args=[unit_slug]) if unit_slug in U.BY_SLUG else f"{reverse('studio:grammar')}?level={g['level']}"
    practice = []
    for p in g["practice"]:
        if p[0] in ("fill", "fix"):
            practice.append({"type": p[0], "prompt": p[1], "accepted": p[2]})
        elif p[0] == "say":
            practice.append({"type": "say", "prompt": p[1]})
        else:
            practice.append({"type": "make", "prompt": p[1], "pattern": p[2]})
    extra = {"lesson": {"hello": g["hello"], "formula": [{"text": t, "cls": ROLE_COLORS.get(r, "")} for t, r in g["formula"]],
                        "rule": g["rule"], "examples": g["examples"], "practice": practice, "slug": slug},
             "unitKey": E.unit_key(unit_slug, 3) if unit_slug in U.BY_SLUG else ""}
    return _player(request, key=E.grammar_key(slug), title=g["title"], title_bn=g["title_bn"], mode="grammar", back=back, extra=extra)


# ------------------------------------------------------------------ Pronunciation course and stories

def _practice_items(practice):
    out = []
    for p in practice:
        if p[0] in ("fill", "fix"):
            out.append({"type": p[0], "prompt": p[1], "accepted": p[2]})
        elif p[0] == "say":
            out.append({"type": "say", "prompt": p[1]})
        else:
            out.append({"type": "make", "prompt": p[1], "pattern": p[2]})
    return out


def _drill_items(drill):
    return [_repeat_item(text, sound=sound, bn=bn, ipa=ipa) for text, sound, bn, ipa in drill]


@learner_required
def pronunciation(request):
    done = E.done_keys(request.learner)
    stages = []
    for code, icon, title, title_bn in PR.STAGES:
        lessons = [{**p, "done": PR.key(p["slug"]) in done, "drilled": PR.drill_key(p["slug"]) in done}
                   for p in PR.by_stage(code)]
        stages.append({"code": code, "icon": icon, "title": title, "title_bn": title_bn, "lessons": lessons})
    total = len(PR.LESSONS)
    finished = sum(1 for p in PR.LESSONS if PR.key(p["slug"]) in done)
    nxt = next((p for p in PR.LESSONS if PR.key(p["slug"]) not in done), None)
    return render(request, "studio/pronunciation.html", {
        "stages": stages, "done": finished, "total": total, "next": nxt, "paid": request.family.has_full_access,
        "free": PR.FREE, "story_count": len(ST.STORIES)})


@learner_required
def pron_lesson(request, slug):
    p = PR.BY_SLUG.get(slug) or _404()
    if not (request.family.has_full_access or slug in PR.FREE):
        return locked(request, "Pronunciation course", "উচ্চারণ কোর্স")
    extra = {"lesson": {"hello": p["hello"], "formula": [{"text": t, "cls": ROLE_COLORS.get(r, "")} for t, r in p["formula"]],
                        "rule": p["rule"], "examples": p["examples"], "practice": _practice_items(p["practice"]), "slug": slug},
             "next": reverse("studio:pron_drill", args=[slug])}
    return _player(request, key=PR.key(slug), title=p["title"], title_bn=p["title_bn"], mode="grammar",
                   back=reverse("studio:pronunciation"), extra=extra)


@learner_required
def pron_drill(request, slug):
    p = PR.BY_SLUG.get(slug) or _404()
    if not (request.family.has_full_access or slug in PR.FREE):
        return locked(request, "Pronunciation course", "উচ্চারণ কোর্স")
    return _player(request, key=PR.drill_key(slug), title=f"{p['title']} · drill", title_bn=f"{p['title_bn']} · অনুশীলন",
                   mode="repeat", items=_drill_items(p["drill"]), back=reverse("studio:pronunciation"))


@learner_required
def stories(request):
    done = E.done_keys(request.learner)
    items = [{**st, "done": ST.key(st["slug"]) in done, "quiz_done": ST.quiz_key(st["slug"]) in done}
             for st in ST.STORIES]
    return render(request, "studio/stories.html", {"stories": items, "paid": request.family.has_full_access,
                                                   "free": ST.FREE, "shadowing": PR.BY_SLUG["pron-shadowing"]})


@learner_required
def story(request, slug):
    st = ST.BY_SLUG.get(slug) or _404()
    if not (request.family.has_full_access or slug in ST.FREE):
        return locked(request, "Stories", "গল্প")
    from world.content import helper
    from world.middleware import helper_lang
    hl = helper_lang(request)
    lines = [{"en": en, "help": helper(en, bn, hl), "note": note} for en, bn, note in st["lines"]]
    vocab = [{"word": w, "meaning": m, "help": helper(m, bn, hl) if hl != "bn" else bn} for w, m, bn in st["vocab"]]
    return render(request, "studio/story.html", {"story": st, "lines": lines, "vocab": vocab})


@learner_required
def story_shadow(request, slug):
    st = ST.BY_SLUG.get(slug) or _404()
    if not (request.family.has_full_access or slug in ST.FREE):
        return locked(request, "Stories", "গল্প")
    items = []
    for en, bn, note in st["lines"]:
        it = _repeat_item(en, bn=bn)
        it["tip_en"], it["tip_bn"] = f"Copy the flow: {note}", f"যেভাবে বলবেন: {note}"
        items.append(it)
    return _player(request, key=ST.key(slug), title=st["title"], title_bn=st["title_bn"], mode="repeat", items=items,
                   back=reverse("studio:story", args=[slug]), extra={"advancedDefault": True})


@learner_required
def story_quiz(request, slug):
    st = ST.BY_SLUG.get(slug) or _404()
    if not (request.family.has_full_access or slug in ST.FREE):
        return locked(request, "Stories", "গল্প")
    vocab = "; ".join(f"{w} — {m}" for w, m, _ in st["vocab"])
    vocab_bn = "; ".join(f"{w} — {bn}" for w, _, bn in st["vocab"])
    lesson = {"hello": (f"Let's check the new words from '{st['title']}'.", f"'{st['title_bn']}' গল্পের নতুন শব্দগুলো যাচাই করি।"),
              "formula": [], "rule": (vocab, vocab_bn),
              "examples": [(en, bn) for en, bn, _ in st["lines"][:2]],
              "practice": _practice_items(st["quiz"]), "slug": f"story-{slug}"}
    return _player(request, key=ST.quiz_key(slug), title=f"{st['title']} · word quiz", title_bn=f"{st['title_bn']} · শব্দ কুইজ",
                   mode="grammar", back=reverse("studio:story", args=[slug]), extra={"lesson": lesson})


# ------------------------------------------------------------------ Coach

@learner_required
def coach(request):
    cat = request.GET.get("c", "all")
    items = [c for c in C.COACHES if cat == "all" or c["category"] == cat]
    return render(request, "studio/coach.html", {"coaches": items, "cat": cat, "categories": C.CATEGORIES,
                                                 "popular": C.BY_SLUG["pronunciation"], "paid": request.family.has_full_access})


@learner_required
def coach_detail(request, slug):
    c = C.BY_SLUG.get(slug) or _404()
    if c["tool"]:
        return redirect(c["tool"])
    done = E.done_keys(request.learner)
    scen = [{**s, "done": f"coach:{slug}:{s['slug']}" in done} for s in c["scenarios"]]
    from practice import ai
    return render(request, "studio/coach_detail.html", {"c": c, "scenarios": scen, "ai_on": ai.enabled(),
                                                        "ai_left": ai.left_today(request.learner) if ai.enabled() else 0})


@paid_required("Coach role-plays", "কোচের রোল-প্লে")
def coach_play(request, slug, scen):
    c, s = C.scenario(slug, scen)
    if not s:
        raise Http404
    from practice import ai
    lines = [{"bot": b, "reply": r, "hint": ""} for b, r in s["lines"]]
    return _player(request, key=f"coach:{slug}:{scen}", title=s["title"], title_bn=s["title_bn"], mode="convo",
                   back=reverse("studio:coach_detail", args=[slug]),
                   extra={"lines": lines, "setting": s["setting"], "persona": s["persona"], "coach": slug, "scenario": scen,
                          "aiOn": ai.enabled() and request.GET.get("free") == "1"})


# ------------------------------------------------------------------ Pronunciation coach

def _sound_bank():
    bank = {}
    for u in U.UNITS:
        for w in u["words"]:
            p = U.parse_word(w)
            bank.setdefault(p["sound"], {"words": [], "phrases": []})["words"].append(w)
        for text, sound, bn in u["phrases"]:
            bank.setdefault(sound, {"words": [], "phrases": []})["phrases"].append((text, sound, bn))
    return bank


@learner_required
def sounds(request):
    bank = _sound_bank()
    done = E.done_keys(request.learner)
    tiles = [{"code": code, "tip_en": S.SOUNDS[code][0], "tip_bn": S.SOUNDS[code][1], "count": len(bank[code]["words"]) + len(bank[code]["phrases"]),
              "example": (U.parse_word(bank[code]["words"][0])["text"] if bank[code]["words"] else bank[code]["phrases"][0][0]),
              "done": f"sound:{code}" in done} for code in S.SOUNDS if code in bank]
    return render(request, "studio/sounds.html", {"tiles": tiles, "paid": request.family.has_full_access})


@paid_required("Pronunciation coach", "উচ্চারণ কোচ")
def sound_drill(request, code):
    bank = _sound_bank().get(code) or _404()
    items = _word_items(bank["words"][:8]) + _phrase_items(bank["phrases"][:4])
    return _player(request, key=f"sound:{code}", title=f"The /{code}/ sound", title_bn=f"/{code}/ ধ্বনি", mode="repeat",
                   items=items, back=reverse("studio:sounds"))


# ------------------------------------------------------------------ Speech analyzer and rehearsal

ANALYZER_PROMPTS = [
    ("Introduce yourself in one minute.", "এক মিনিটে নিজের পরিচয় দিন।"),
    ("Describe your favourite place in Bangladesh.", "বাংলাদেশে আপনার প্রিয় জায়গার বর্ণনা দিন।"),
    ("Talk about a person you admire and why.", "আপনি যাকে শ্রদ্ধা করেন তার কথা বলুন।"),
    ("What did you do last weekend?", "গত সপ্তাহান্তে কী করেছিলেন?"),
    ("Give a one-minute talk: Why should everyone learn English?", "এক মিনিটের বক্তৃতা: সবার কেন ইংরেজি শেখা উচিত?"),
    ("Explain how to cook your favourite dish.", "প্রিয় খাবার রান্নার নিয়ম বলুন।"),
    ("Persuade us: Is it better to live in a city or a village?", "বোঝান: শহর না গ্রাম — কোথায় থাকা ভালো?"),
    ("Tell a short story about a time you were brave.", "এমন একটা সময়ের গল্প বলুন যখন আপনি সাহস দেখিয়েছিলেন।"),
]


@paid_required("Speech analyzer", "স্পিচ অ্যানালাইজার")
def analyzer(request):
    i = request.GET.get("p")
    i = int(i) if i and i.isdigit() and int(i) < len(ANALYZER_PROMPTS) else random.randrange(len(ANALYZER_PROMPTS))
    prompt = ANALYZER_PROMPTS[i]
    history = Attempt.objects.filter(learner=request.learner, kind="speech")[:8]
    return _player(request, key=f"speech:{timezone.localdate():%Y%m%d}", title="Speech analyzer", title_bn="স্পিচ অ্যানালাইজার",
                   mode="speak", back=reverse("studio:coach"),
                   extra={"prompt": prompt[0], "promptBn": prompt[1], "seconds": 90, "minWords": 60, "targetWpm": 120,
                          "prompts": [p[0] for p in ANALYZER_PROMPTS], "promptIndex": i,
                          "history": [{"when": a.created_at.strftime("%d %b"), "score": a.score, "wpm": a.wpm} for a in history]})


@paid_required("Presentation coach", "প্রেজেন্টেশন কোচ")
def rehearse(request):
    text = request.POST.get("text", "").strip() if request.method == "POST" else ""
    if not text:
        return render(request, "studio/rehearse.html", {})
    import re
    lines = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if len(s.strip().split()) >= 2][:30]
    return _player(request, key="rehearse", title="Presentation rehearsal", title_bn="প্রেজেন্টেশন অনুশীলন", mode="repeat",
                   items=_sentence_items(lines), back=reverse("studio:rehearse"), extra={"advancedDefault": True})


# ------------------------------------------------------------------ IELTS

@learner_required
def ielts(request):
    done = E.done_keys(request.learner)
    bands = []
    for band, info in I.BANDS.items():
        keys = [E.ielts_key(band, t["slug"], n) for t in I.units_for(band) for n, *_ in I.LESSONS]
        d = sum(1 for k in keys if k in done)
        bands.append({"band": band, **info, "done": d, "total": len(keys), "percent": round(d * 100 / len(keys))})
    sc = E.scores(request.learner)
    return render(request, "studio/ielts.html", {"bands": bands, "scores": sc, "paid": request.family.has_full_access})


@learner_required
def ielts_band(request, band):
    info = I.BANDS.get(band) or _404()
    done = E.done_keys(request.learner)
    units = []
    for i, t in enumerate(I.units_for(band), 1):
        d = sum(1 for n, *_ in I.LESSONS if E.ielts_key(band, t["slug"], n) in done)
        units.append({"i": i, **t, "done": d, "total": len(I.LESSONS), "percent": round(d * 100 / len(I.LESSONS))})
    return render(request, "studio/ielts_band.html", {"band": band, "info": info, "units": units, "paid": request.family.has_full_access})


@learner_required
def ielts_unit(request, band, topic):
    info = I.BANDS.get(band) or _404()
    t = I.BY_SLUG.get(topic) or _404()
    if topic not in I.COURSE[band]:
        raise Http404
    done = E.done_keys(request.learner)
    nxt = next((n for n, *_ in I.LESSONS if E.ielts_key(band, topic, n) not in done), None)
    diff = {6: ["Easy", "Medium", "Medium"], 7: ["Medium", "Medium", "Difficult"], 8: ["Medium", "Difficult", "Difficult"]}[band]
    lessons = [{"n": n, "kind": k, "title": tt, "title_bn": tbn, "icon": ic, "difficulty": diff[n - 1],
                "done": E.ielts_key(band, topic, n) in done, "next": n == nxt} for n, k, tt, tbn, ic in I.LESSONS]
    return render(request, "studio/ielts_unit.html", {"band": band, "info": info, "t": t, "lessons": lessons,
                                                      "collocations": I.collocations(t, band)})


@paid_required("IELTS speaking courses", "IELTS স্পিকিং কোর্স")
def ielts_lesson(request, band, topic, n):
    info = I.BANDS.get(band) or _404()
    t = I.BY_SLUG.get(topic) or _404()
    if topic not in I.COURSE[band]:
        raise Http404
    key = E.ielts_key(band, topic, n)
    back = reverse("studio:ielts_unit", args=[band, topic])
    title = f"{t['title']} (Part {t['part']})"
    if n == 1:
        return _player(request, key=key, title=title, title_bn=t["title_bn"], mode="repeat",
                       items=_sentence_items(I.collocations(t, band)), back=back)
    if n == 2:
        return _player(request, key=key, title=title, title_bn=t["title_bn"], mode="repeat",
                       items=_sentence_items(t["model"]), back=back, extra={"advancedDefault": band >= 8})
    part = t["part"]
    return _player(request, key=key, title=title, title_bn=t["title_bn"], mode="speak", back=back,
                   extra={"prompt": t["questions"][0], "questions": t["questions"], "ielts": True, "part": part,
                          "prep": 60 if part == 2 else 0, "seconds": 120 if part == 2 else 60 if part == 3 else 40,
                          "minWords": {1: 35, 2: 160, 3: 70}[part], "targetWpm": info["wpm"]})


# ------------------------------------------------------------------ Discover

@learner_required
def discover(request):
    from . import shorts as SH
    short_topics = [(k, en, bn, (em, SH.SKY.get(k, SH.SKY["out"]))) for k, en, bn, em in SH.TOPICS
                    if k != "videos" or SH.videos()]
    return render(request, "studio/discover.html", {"word": _word_of_day(), "short_topics": short_topics,
                                                    "shorts_today": SH.done_today(request.learner),
                                                    "bookmarks": request.learner.bookmarks.all()[:6],
                                                    "bookmark_count": request.learner.bookmarks.count()})


@learner_required
def dictionary(request):
    from practice.models import VocabWord
    q = request.GET.get("q", "").strip()[:60]
    results = []
    if q:
        seen = set()
        for w in VocabWord.objects.filter(word__iexact=q).order_by("rank")[:3] or VocabWord.objects.filter(word__istartswith=q).order_by("rank")[:12]:
            if w.word.lower() in seen:
                continue
            seen.add(w.word.lower())
            results.append(w)
    saved = set(request.learner.bookmarks.values_list("text", flat=True))
    return render(request, "studio/dictionary.html", {"q": q, "results": results, "saved": saved})


@learner_required
def my_words(request):
    marks = list(request.learner.bookmarks.all())
    if request.GET.get("practise") and marks:
        if not request.family.has_full_access:
            return locked(request, "Vocabulary coach", "শব্দভান্ডার কোচ")
        items = [_repeat_item(b.text, bn=b.meaning_bn, ipa=b.ipa) for b in marks[:15]]
        return _player(request, key=f"mywords:{timezone.localdate():%Y%m%d}", title="My Words", title_bn="আমার শব্দ",
                       mode="repeat", items=items, back=reverse("studio:my_words"))
    return render(request, "studio/my_words.html", {"marks": marks})


# ------------------------------------------------------------------ Progress

@learner_required
def progress(request):
    from growth import engine as growth
    learner = request.learner
    sc = E.scores(learner)
    secs = E.learning_seconds(learner)
    badges = E.all_badges(learner)
    return render(request, "studio/progress.html", {
        "scores": sc, "pent": E.pentagon(sc), "journey": E.journey(learner, sc),
        "hours": secs // 3600, "mins": (secs % 3600) // 60, "lessons": E.lessons_count(learner),
        "week": E.week(learner), "history": LessonDone.objects.filter(learner=learner)[:12],
        "badges_earned": [b for b in badges if b["earned"]], "badges_next": sorted([b for b in badges if not b["earned"]], key=lambda b: -b["percent"])[:4],
        "badge_count": sum(1 for b in badges if b["earned"]), "badge_total": len(badges),
        "certificates": learner.certificates.all(), "streak": growth.streak_info(learner), "xp": growth.xp_panel(learner),
        "wallet": E.wallet(learner),
    })


@learner_required
def badges(request):
    return render(request, "studio/badges.html", {"badges": E.all_badges(request.learner)})


@learner_required
def certificate(request, number):
    cert = get_object_or_404(Certificate, number=number, learner__family=request.family)
    return render(request, "studio/certificate.html", {"cert": cert})


@learner_required
@require_POST
def buy_freeze(request):
    from django.contrib import messages
    w = E.wallet(request.learner)
    month = timezone.localdate().strftime("%Y-%m")
    if w.freeze_month != month:
        w.freeze_month, w.extra_freezes = month, 0
    if w.extra_freezes >= 2:
        messages.warning(request, "You can buy at most 2 extra streak freezes a month.")
    elif w.gems < 20:
        messages.warning(request, "You need 20 gems for a streak freeze. Finish lessons to earn more.")
    else:
        w.gems -= 20
        w.extra_freezes += 1
        messages.success(request, "Streak freeze bought! A missed day this month won't break your streak.")
    w.save()
    return redirect("studio:progress")


@learner_required
def more(request):
    return render(request, "studio/more.html", {})


# ------------------------------------------------------------------ JSON API used by the player

def _body(request):
    try:
        return json.loads(request.body or "{}")
    except ValueError:
        return {}


def _api_learner(view):
    from functools import wraps

    @wraps(view)
    @learner_required
    @require_POST
    def inner(request, *a, **k):
        return view(request, _body(request), *a, **k)
    return inner


@_api_learner
def api_attempt(request, d):
    kind = d.get("kind", "repeat")
    if kind not in Attempt.Kind.values:
        kind = "repeat"
    target, said = d.get("target", ""), d.get("said", "")
    if kind in ("repeat", "convo", "words") and target:
        score = E.speech_score(target, said, d.get("confidence")) if said else int(d.get("score") or 0)
        if d.get("free") and said:  # learner's own answer in a conversation
            n = len(E.words(said))
            score = max(score, min(95, 55 + n * 5)) if n >= 3 else score
    else:
        score = int(d.get("score") or 0)
    a = E.record(request.learner, kind, d.get("key", ""), target, said, score, d.get("seconds", 0), d.get("wpm", 0))
    return JsonResponse({"score": a.score, "marks": E.word_marks(target, said) if said and target else []})


@_api_learner
def api_finish(request, d):
    key = d.get("key", "")
    if not key:
        return JsonResponse({"ok": False}, status=400)
    score = max(0, min(100, int(d.get("score") or 0)))
    done, first = E.finish(request.learner, key, d.get("title", ""), score)
    extra_key = d.get("alsoKey")
    if extra_key and extra_key.startswith("unit:"):
        E.finish(request.learner, extra_key, d.get("title", ""), score)
    gems = E.wallet(request.learner).gems
    return JsonResponse({"ok": True, "first": first, "score": done.score, "gems": gems,
                         "xp": 20 + score // 5 if first else 0, "gemsEarned": (5 if score >= 90 else 2) if first else 0})


@_api_learner
def api_bookmark(request, d):
    text = (d.get("text") or "").strip()[:120]
    if not text:
        return JsonResponse({"ok": False}, status=400)
    b = Bookmark.objects.filter(learner=request.learner, text=text).first()
    if b:
        b.delete()
        return JsonResponse({"ok": True, "saved": False})
    Bookmark.objects.create(learner=request.learner, text=text, ipa=(d.get("ipa") or "")[:80], meaning_bn=(d.get("bn") or "")[:120])
    return JsonResponse({"ok": True, "saved": True})


@_api_learner
def api_check(request, d):
    """Grammar, pronunciation and story-quiz practice: check a typed or spoken answer."""
    slug = d.get("lesson", "")
    g, key, kind = G.BY_SLUG.get(slug), E.grammar_key(slug), "grammar"
    if g is None and slug in PR.BY_SLUG:
        g, key = PR.BY_SLUG[slug], PR.key(slug)
    elif g is None and slug.startswith("story-") and slug[6:] in ST.BY_SLUG:
        st = ST.BY_SLUG[slug[6:]]
        g, key, kind = {"slug": slug, "practice": st["quiz"]}, ST.quiz_key(slug[6:]), "words"
    i = int(d.get("index") or 0)
    if not g or not 0 <= i < len(g["practice"]):
        return JsonResponse({"ok": False}, status=400)
    item = g["practice"][i]
    answer = d.get("answer", "")
    ai_note, ai_used = "", False
    if item[0] in ("fill", "fix"):
        ok = E.check_typed(answer, item[2])
        score = 100 if ok else 0
        right = item[2][0]
        if item[0] == "fill" and not ok:
            right = item[1].replace("___", item[2][0])
    elif item[0] == "say":
        score = E.speech_score(item[1], answer, d.get("confidence"))
        ok, right = score >= 70, item[1]
    else:
        ok = E.check_pattern(answer, item[2])
        score, right = (90 if ok else 30), ""
        from practice import ai
        if answer and ai.enabled() and ai.left_today(request.learner):
            ai_note = ai.ask(ai.SAFETY + " You are a grammar coach. The task was: " + item[1] +
                             " Reply in at most 2 short sentences: say if the sentence is correct, give a corrected version if needed, "
                             "then one Bangla sentence of encouragement.", [{"role": "user", "content": answer[:300]}], max_tokens=160) or ""
            ai_used = bool(ai_note)
    if kind == "grammar" and item[0] == "say" and key.startswith("pron:"):
        kind = "repeat"
    E.record(request.learner, kind, key, item[1], answer, score, d.get("seconds", 0), ai_used=ai_used)
    return JsonResponse({"ok": ok, "score": score, "right": right, "ai": ai_note})


@_api_learner
def api_analyse(request, d):
    res = E.analyse_speech(d.get("transcript", ""), d.get("seconds", 0), int(d.get("targetWpm") or 120), int(d.get("minWords") or 40))
    from world.content import ui_pair
    from world.middleware import current_lang
    ui = current_lang(request)
    res["tips"] = [ui_pair(en, bn, ui) for en, bn in res["tips"]]
    kind = "ielts" if d.get("ielts") else "speech"
    if (d.get("key") or "").startswith("unit:"):
        kind = "speech"
    res["ai"] = ""
    from practice import ai
    ai_used = False
    if res["words"] >= 15 and ai.enabled() and ai.left_today(request.learner):
        note = ai.ask(ai.SAFETY + " You are a speaking coach. The learner answered: '" + (d.get("prompt") or "")[:200] +
                      "'. Give 3 short bullet points: one thing done well, one grammar correction (quote and fix), one better word or phrase. "
                      "Finish with one short Bangla sentence.", [{"role": "user", "content": d.get("transcript", "")[:1500]}], max_tokens=260)
        if note:
            res["ai"], ai_used = note, True
    E.record(request.learner, kind, d.get("key", "speech"), (d.get("prompt") or "")[:200], d.get("transcript", ""),
             res["overall"], res["seconds"], res["wpm"], ai_used=ai_used)
    return JsonResponse(res)


@_api_learner
def api_reply(request, d):
    """Free talk with a coach (AI). Without AI, the scripted lines are used instead."""
    from practice import ai
    c, s = C.scenario(d.get("coach", ""), d.get("scenario", ""))
    if not s or not ai.enabled() or not ai.left_today(request.learner):
        return JsonResponse({"reply": None})
    history = [m for m in d.get("history", []) if m.get("role") in ("user", "assistant")][-10:]
    system = (ai.SAFETY + f" Role-play: you are {s['persona']}. Setting: {s['setting']}. Stay in role, reply in 1–2 short, natural "
              "British English sentences, then ask a question to keep the conversation going. If the learner makes a clear mistake, "
              "add a short correction in brackets at the end, like (Tip: say 'I have been' not 'I am been').")
    reply = ai.ask(system, [{"role": m["role"], "content": str(m.get("content", ""))[:400]} for m in history], max_tokens=140)
    if reply:
        E.record(request.learner, "coach", f"coach:{c['slug']}:{s['slug']}", "free talk", history[-1]["content"] if history else "",
                 70, 0, ai_used=True)
    return JsonResponse({"reply": reply})


def _404():
    raise Http404


# ------------------------------------------------------------------ Short videos (watch, then say it back)

@learner_required
def shorts(request):
    from world.content import js_i18n

    from . import shorts as SH
    topic = request.GET.get("t", "all")
    if topic not in SH.TOPIC_KEYS:
        topic = "all"
    counts = SH.counts()
    counts["videos"] = len(SH.videos())
    return render(request, "studio/shorts.html", {
        "topics": SH.TOPICS, "topic": topic, "counts": counts, "paid": request.family.has_full_access,
        "free_per_day": SH.FREE_PER_DAY, "done_today": SH.done_today(request.learner),
        "cfg": {"topic": topic, "start": request.GET.get("s", ""), "lang": _lang(request), "paid": request.family.has_full_access,
                "feedUrl": reverse("studio:api_shorts"), "tryUrl": reverse("studio:api_short_try"),
                "bookmarkUrl": reverse("studio:api_bookmark"), "payUrl": reverse("core:pricing"),
                "i18n": js_i18n(request)},
    })


@learner_required
def api_shorts(request):
    from . import shorts as SH
    try:
        offset = max(0, int(request.GET.get("o", 0)))
    except ValueError:
        offset = 0
    items, more, total = SH.feed(request.learner, request.GET.get("t", "all"), offset)
    first = request.GET.get("s")
    if first and offset == 0:
        s = SH.by_id(first)
        if s:
            items = [{**s, "mastered": False}] + [x for x in items if x["id"] != first]
    from world.content import localize_short
    items = [localize_short(x, request) for x in items]
    return JsonResponse({"items": items, "more": more, "next": offset + SH.PAGE, "total": total})


@_api_learner
def api_short_try(request, d):
    from growth import engine as growth

    from . import shorts as SH
    s = SH.by_id(str(d.get("id", "")))
    if not s:
        return JsonResponse({"ok": False}, status=404)
    key = f"short:{s['id']}"
    learner = request.learner
    if not request.family.has_full_access:
        tried = Attempt.objects.filter(learner=learner, kind="short", key=key,
                                       created_at__date=timezone.localdate()).exists()
        if not tried and SH.done_today(learner) >= SH.FREE_PER_DAY:
            return JsonResponse({"locked": True})
    said = d.get("said", "")
    score = E.speech_score(s["line"], said, d.get("confidence")) if said else int(d.get("score") or 0)
    E.record(learner, "short", key, s["line"], said, score, d.get("seconds", 5))
    xp = 0
    if score >= 70 and growth.award(learner, 5, "Short video", key=f"{key}:{timezone.localdate():%Y%m%d}"[:80]):
        xp = 5
    return JsonResponse({"score": score, "marks": E.word_marks(s["line"], said) if said else [], "xp": xp,
                         "today": SH.done_today(learner)})
