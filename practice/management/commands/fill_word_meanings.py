"""Add Bangla meanings, a simple English definition and an example sentence to the word lists.

Uses the site's AI key (FE_AI_API_KEY) with the low-cost model, 40 words per request.
About 8,000 different words in all: well under one US dollar with Claude Haiku. Safe to stop and run
again: only words without a Bangla meaning are sent.

    python manage.py fill_word_meanings --limit 2000
"""

import json

from django.core.management.base import BaseCommand

from django.db.models import Q

from practice import ai
from practice.models import VocabWord

SYSTEM = (
    "You write a learner's dictionary for Bangladeshi children and parents learning British English. "
    "For each English word give: bn = the common Bangla meaning (1-4 words, Bangla script), "
    "def = a very simple English definition (max 10 words), ex = one short natural example sentence "
    "in British English that a child could understand (max 10 words, British spelling). "
    "Use the part of speech given. Reply with JSON only: {\"word\": {\"bn\": \"...\", \"def\": \"...\", \"ex\": \"...\"}}"
)


class Command(BaseCommand):
    help = "Fill Bangla meanings and examples for the 3000/7000 word lists with AI."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=1000, help="Most words to fill this run")
        parser.add_argument("--batch", type=int, default=40)

    def handle(self, *args, limit, batch, **opts):
        if not ai.enabled():
            self.stderr.write("Set FE_AI_API_KEY first (see .env.example).")
            return
        todo = []
        for w in VocabWord.objects.filter(Q(meaning_bn="") | Q(definition="")).exclude(deck__series="").order_by("rank"):
            if w.word not in {t[0] for t in todo}:
                todo.append((w.word, w.pos))
            if len(todo) >= limit:
                break
        done = 0
        for i in range(0, len(todo), batch):
            part = todo[i:i + batch]
            msg = "\n".join(f"{w} ({p})" for w, p in part)
            reply = ai.ask(SYSTEM, [{"role": "user", "content": msg}], max_tokens=4000) or ""
            try:
                data = json.loads(reply[reply.index("{"): reply.rindex("}") + 1])
            except ValueError:
                self.stderr.write(f"Could not read the reply for batch {i // batch + 1}; will retry next run.")
                continue
            for word, _ in part:
                d = data.get(word) or data.get(word.lower())
                if not d or not d.get("bn"):
                    continue
                n = VocabWord.objects.filter(word=word, meaning_bn="").update(meaning_bn=d["bn"][:120])
                VocabWord.objects.filter(word=word, definition="").update(definition=(d.get("def") or "")[:200])
                VocabWord.objects.filter(word=word, example="").update(example=(d.get("ex") or "")[:200])
                done += 1
            self.stdout.write(f"{min(i + batch, len(todo))}/{len(todo)} words sent")
        left = VocabWord.objects.filter(Q(meaning_bn="") | Q(definition="")).exclude(
            deck__series="").values("word").distinct().count()
        self.stdout.write(self.style.SUCCESS(f"Filled {done} words. Still without a meaning: {left}."))
