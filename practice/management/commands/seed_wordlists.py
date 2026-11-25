"""Load the 3000 and 7000 most frequent English words into weekly practice sets.

kids3000: 156 weekly sets (≈19 words a week for 3 years)
core7000: 104 weekly sets (≈67 words a week for 2 years)

The lists are built from open data (see tools/build_wordlists.py) and carry British IPA. Bangla
meanings and example sentences are added by `python manage.py fill_word_meanings` (AI) or by hand in
/admin; meanings already filled in are kept when this command is run again.
"""

import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from practice.models import VocabDeck, VocabWord

DATA = Path(__file__).resolve().parents[2] / "data"
WEEKS = {"kids3000": 156, "core7000": 104}


def level_for(series, week, weeks):
    part = (week - 1) * 3 // weeks          # 0, 1, 2 = first, middle, last third
    return {"kids3000": (1, 3, 5), "core7000": (4, 6, 8)}[series][part]


class Command(BaseCommand):
    help = "Create the weekly word sets (3000 for children, 7000 for school students and IELTS)."

    @transaction.atomic
    def handle(self, *args, **opts):
        known = {}
        with open(DATA / "bn_meanings.txt", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    word, bn = line.rstrip("\n").split("=", 1)
                    known[word.lower()] = (bn, "", "", "")
        defs = {}
        with open(DATA / "en_definitions.tsv", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                defs[r["word"].lower()] = (r["definition"], r["example"])
        for w in VocabWord.objects.exclude(meaning_bn=""):
            known.setdefault(w.word.lower(), (w.meaning_bn, w.example, w.definition, w.emoji))
        for series, weeks in WEEKS.items():
            with open(DATA / f"{series}.tsv", encoding="utf-8") as f:
                rows = list(csv.DictReader(f, delimiter="\t"))
            n = len(rows)
            for week in range(1, weeks + 1):
                chunk = rows[(week - 1) * n // weeks: week * n // weeks]
                deck, _ = VocabDeck.objects.update_or_create(
                    slug=f"{series}-w{week:03d}",
                    defaults={"title": f"{chunk[0]['word']} … {chunk[-1]['word']}",
                              "title_bn": f"সপ্তাহ {week}", "emoji": "🔤", "series": series, "week": week,
                              "level": level_for(series, week, weeks), "order": 1000 + week})
                keep = set()
                for i, r in enumerate(chunk, 1):
                    meaning, example, definition, emoji = known.get(r["word"].lower(), ("", "", "", ""))
                    d_en, ex_en = defs.get(r["word"].lower(), ("", ""))
                    definition, example = definition or d_en, example or ex_en
                    obj, created = VocabWord.objects.get_or_create(
                        deck=deck, word=r["word"],
                        defaults={"pos": r["pos"], "ipa": r["ipa_gb"], "rank": int(r["rank"]), "order": i,
                                  "meaning_bn": meaning, "example": example, "definition": definition, "emoji": emoji})
                    if not created:
                        obj.pos, obj.ipa, obj.rank, obj.order = r["pos"], r["ipa_gb"], int(r["rank"]), i
                        if not obj.meaning_bn and meaning:
                            obj.meaning_bn = meaning
                        obj.definition = obj.definition or definition
                        obj.example = obj.example or example
                        obj.save(update_fields=["pos", "ipa", "rank", "order", "meaning_bn", "definition", "example"])
                    keep.add(obj.pk)
                deck.words.exclude(pk__in=keep).delete()
            self.stdout.write(f"{series}: {n} words in {weeks} weekly sets")
