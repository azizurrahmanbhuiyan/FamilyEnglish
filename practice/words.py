"""Word weeks: the 3000 (children, parents, grandparents) and 7000 (school students, IELTS) most frequent
English words, a week at a time. Each week: listen and say (British voice, microphone check), meaning in
Bangla, spell what you hear, write sentences, then the words go into the flashcard reviews."""

import re

from django.contrib import messages
from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from core.access import paid_required
from core.utils import learner_required

from . import ai
from .models import LEARNED_BOX, CardReview, SkillCheck, VocabDeck

TRACK_SERIES = {"kid": "kids3000", "elder": "kids3000", "adult": "kids3000", "student": "core7000", "ielts": "core7000"}


def series_for(learner):
    return TRACK_SERIES.get(learner.course_track, "kids3000")


def _free_week(request, slug, *a, **k):
    return slug == "kids3000-w001"            # one sample week is free


def _deck(slug):
    deck = get_object_or_404(VocabDeck, slug=slug)
    if not deck.series:
        raise Http404
    return deck


@learner_required                      # the list is open to all; the weeks lock (except week 1)
def words_home(request):
    learner = request.learner
    series = request.GET.get("list") or series_for(learner)
    if series not in VocabDeck.SERIES:
        series = "kids3000"
    decks = VocabDeck.objects.filter(series=series).order_by("week").annotate(n=Count("words"))
    learned = dict(CardReview.objects.filter(learner=learner, word__deck__series=series, box__gte=LEARNED_BOX)
                   .values_list("word__deck").annotate(c=Count("id")))
    done = set(SkillCheck.objects.filter(learner=learner, kind=SkillCheck.Kind.WORDS)
               .values_list("detail", flat=True))
    rows = [{"deck": d, "learned": learned.get(d.id, 0), "done": d.slug in done,
             "open": request.family.has_full_access or d.slug == "kids3000-w001"} for d in decks]
    total = sum(r["deck"].n for r in rows)
    known = sum(r["learned"] for r in rows)
    nxt = next((r for r in rows if not r["done"]), None)
    return render(request, "practice/words_home.html", {
        "series": series, "series_info": VocabDeck.SERIES, "rows": rows, "total": total, "known": known,
        "percent": round(known * 100 / total) if total else 0, "next": nxt, "mine": series_for(learner)})


@paid_required("Word weeks (3000 and 7000 words)", "সাপ্তাহিক শব্দ (৩০০০ ও ৭০০০ শব্দ)", free_if=_free_week)
def word_week(request, slug):
    deck = _deck(slug)
    words = list(deck.words.all())
    prev = VocabDeck.objects.filter(series=deck.series, week=deck.week - 1).first()
    nxt = VocabDeck.objects.filter(series=deck.series, week=deck.week + 1).first()
    feedback = request.session.pop(f"words-fb-{slug}", None)
    return render(request, "practice/word_week.html", {
        "deck": deck, "words": words, "prev": prev, "next": nxt, "feedback": feedback,
        "spell_words": [w.word for w in words if w.word.isalpha() and len(w.word) > 1][:12],
        "series_info": VocabDeck.SERIES[deck.series]})


def check_sentences(text, words):
    """Simple checks that need no AI: which week words were used, capitals and full stops."""
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]
    low = text.lower()
    used = [w for w in words if re.search(rf"\b{re.escape(w.lower())}", low)]
    notes = []
    for s in sentences:
        if s[0].isalpha() and not s[0].isupper():
            notes.append(f"Start with a capital letter: “{s[:30]}…”")
        if s[-1] not in ".!?":
            notes.append(f"End with a full stop: “…{s[-30:]}”")
        if re.search(r"\bi\b", s):
            notes.append("Write 'I' (me) as a capital letter.")
    american = {"color": "colour", "favorite": "favourite", "center": "centre", "neighbor": "neighbour",
                "mom": "mum", "realize": "realise", "organize": "organise", "theater": "theatre",
                "program": "programme", "traveling": "travelling", "gray": "grey"}
    for us, gb in american.items():
        if re.search(rf"\b{us}\b", low):
            notes.append(f"British spelling: write '{gb}', not '{us}'.")
    return sentences, used, notes[:6]


@require_POST
@paid_required("Word weeks (3000 and 7000 words)", "সাপ্তাহিক শব্দ (৩০০০ ও ৭০০০ শব্দ)", free_if=_free_week)
def word_write(request, slug):
    deck = _deck(slug)
    text = (request.POST.get("text") or "").strip()[:1500]
    words = [w.word for w in deck.words.all()]
    sentences, used, notes = check_sentences(text, words)
    fb = {"text": text, "used": used, "notes": notes, "n": len(sentences), "ai": ""}
    if text and request.family.has_full_access and ai.enabled() and ai.left_today(request.learner) > 0:
        fb["ai"] = ai.ask(
            "You are a kind English teacher in Bangladesh. The learner wrote sentences using new words. "
            "Correct them to natural British English (British spelling). Reply in this form: the corrected "
            "sentences, then up to three short tips, each with a Bangla explanation in brackets. Be brief and warm.",
            [{"role": "user", "content": text}], max_tokens=400) or ""
    request.session[f"words-fb-{slug}"] = fb
    if len(used) >= 3:
        messages.success(request, f"You used {len(used)} of this week's words. Well done!")
    return redirect(f"{request.path.rsplit('/write', 1)[0]}/#write")


@require_POST
@paid_required("Word weeks (3000 and 7000 words)", "সাপ্তাহিক শব্দ (৩০০০ ও ৭০০০ শব্দ)", free_if=_free_week)
def word_done(request, slug):
    from growth.engine import award
    from learning.planner import tick_days

    deck = _deck(slug)
    try:
        score = int(request.POST.get("score", 0))
        total = int(request.POST.get("total", 0))
    except ValueError:
        score = total = 0
    total = max(0, min(total, 20))
    score = max(0, min(score, total))
    learner = request.learner
    SkillCheck.objects.create(learner=learner, kind=SkillCheck.Kind.WORDS, skill="vocabulary",
                              score=score, total=total, detail=deck.slug)
    today = timezone.localdate()
    for w in deck.words.all():                      # this week's words join the flashcard reviews
        CardReview.objects.get_or_create(learner=learner, word=w, defaults={"due": today})
    award(learner, 40, "word week", key=f"words-{deck.slug}")
    tick_days(learner, deck=deck)
    messages.success(request, f"Week {deck.week} done: {score}/{total} spelled right. "
                              "The words are now in your flashcards for review.")
    nxt = VocabDeck.objects.filter(series=deck.series, week=deck.week + 1).first()
    return redirect("practice:word_week", slug=nxt.slug) if nxt else redirect("practice:words")
