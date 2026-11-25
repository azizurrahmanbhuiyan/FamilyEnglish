from django.core.management.base import BaseCommand

from learning.family_talk import from_tuples
from learning.models import TalkTopic
from learning.seed.talk_topics_daily import DAILY
from learning.seed.talk_topics_study import STUDY

TRIPS = {"zoo", "botanical-garden", "amusement-park", "museum", "sea-beach", "historical-places"}


class Command(BaseCommand):
    help = "Load the 'Talk at home' theme lessons: daily life, topics and trips."

    def handle(self, *args, **options):
        n = 0
        for group_rows, default_group in ((DAILY, "daily"), (STUDY, "study")):
            for order, t in enumerate(group_rows, 1):
                group = "trip" if t["slug"] in TRIPS else default_group
                TalkTopic.objects.update_or_create(slug=t["slug"], defaults={
                    "group": group, "order": order, "emoji": t["emoji"], "title": t["title"],
                    "title_bn": t["title_bn"], "intro_bn": t.get("intro_bn", ""),
                    "words": [{"word": w, "emoji": e, "bn": bn} for w, e, bn in t["words"]],
                    "rhyme": t.get("rhyme", ""), "rhyme_note": t.get("rhyme_note", ""),
                    "family_talk": from_tuples(t["talk"]),
                })
                n += 1
        if options.get("verbosity", 1):
            self.stdout.write(self.style.SUCCESS(f"Talk at home: {n} theme lessons ready."))
