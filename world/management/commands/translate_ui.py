"""Translate FamilyEnglish into other languages with the AI key (FE_AI_API_KEY) and save the result.

    python manage.py translate_ui --pending            # texts people have seen but not yet translated (run by cron)
    python manage.py translate_ui --lang hi --all      # the whole site into Hindi (~1,500 texts, a few minutes)
    python manage.py translate_ui --lang hi --all --dry-run   # just count

Hand-written translations (world/locale/<lang>.json) and texts edited in /admin are never replaced.
Suggested cPanel cron job (every 10 minutes):
    cd ~/familyenglish && ~/virtualenv/familyenglish/3.13/bin/python manage.py translate_ui --pending --quiet
"""

import json
import re

from django.core.management.base import BaseCommand, CommandError

from practice import ai
from world import translate
from world.data import CODES, english_name
from world.models import UiText
from world.sources import all_strings

BATCH = 40
SYSTEM = (
    "You translate the user interface and lesson explanations of FamilyEnglish, a friendly app where families "
    "learn to speak English. Translate each English text into {lang}. Use simple, warm, everyday words that a "
    "parent or grandparent understands. Keep emoji, numbers, symbols like ✓ → · / and HTML tags exactly. "
    "Keep these in English: FamilyEnglish, IELTS, CEFR, XP, A1, A2, B1, B2, C1, C2, OTP, bKash, Nagad, Doel, "
    "and any English example word or sentence that the learner must say (inside quotes). "
    "Reply with ONLY a JSON array of strings, the same length and order as the input array."
)


class Command(BaseCommand):
    help = "Translate site texts into other languages using the AI key and save them."

    def add_arguments(self, parser):
        parser.add_argument("--lang", action="append", default=[], help="Language code, e.g. hi, ar, es (can repeat)")
        parser.add_argument("--all", action="store_true", help="Translate every text on the site, not only pending ones")
        parser.add_argument("--pending", action="store_true", help="Translate texts waiting in every language")
        parser.add_argument("--limit", type=int, default=0, help="At most this many texts per language")
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--quiet", action="store_true")

    def handle(self, *args, **o):
        langs = o["lang"]
        if o["pending"] and not langs:
            langs = sorted(set(UiText.objects.filter(text="").values_list("lang", flat=True)))
        langs = [l for l in langs if l in CODES and l not in ("en", "bn")]
        if not langs:
            if not o["quiet"]:
                self.stdout.write("Nothing to translate.")
            return
        if not o["dry_run"] and not ai.enabled():
            raise CommandError("Set FE_AI_API_KEY in .env first (the same key the AI tutor uses).")
        for lang in langs:
            self._lang(lang, o)

    def _lang(self, lang, o):
        have = translate.table(lang)
        todo = list(UiText.objects.filter(lang=lang, text="").values_list("source", flat=True))
        if o["all"]:
            todo += all_strings()
        seen, items = set(), []
        for s in todo:
            if s and s not in seen and s not in have:
                seen.add(s)
                items.append(s)
        if o["limit"]:
            items = items[:o["limit"]]
        name = english_name(lang)
        if not o["quiet"] or items:
            self.stdout.write(f"{name} ({lang}): {len(items)} to translate")
        if o["dry_run"] or not items:
            return
        done = 0
        for i in range(0, len(items), BATCH):
            chunk = items[i:i + BATCH]
            out = self._ask(chunk, name)
            if not out:
                self.stderr.write(f"  batch {i // BATCH + 1}: no usable answer, skipped (it will be tried again)")
                continue
            for src, txt in zip(chunk, out):
                if not isinstance(txt, str) or not txt.strip():
                    continue
                obj, _ = UiText.objects.get_or_create(lang=lang, key=UiText.key_for(src), defaults={"source": src})
                if obj.origin != UiText.Origin.MANUAL:
                    obj.text, obj.origin = txt.strip(), UiText.Origin.AI
                    obj.save(update_fields=["text", "origin", "updated_at"])
                    done += 1
            if not o["quiet"]:
                self.stdout.write(f"  {min(i + BATCH, len(items))}/{len(items)}")
        translate.forget(lang)
        self.stdout.write(self.style.SUCCESS(f"  saved {done} translations into {name}"))

    def _ask(self, chunk, name):
        reply = ai.ask(SYSTEM.format(lang=name), [{"role": "user", "content": json.dumps(chunk, ensure_ascii=False)}], max_tokens=6000)
        if not reply:
            return None
        m = re.search(r"\[.*\]", reply, re.S)
        try:
            data = json.loads(m.group(0) if m else reply)
        except (ValueError, AttributeError):
            return None
        return data if isinstance(data, list) and len(data) == len(chunk) else None
