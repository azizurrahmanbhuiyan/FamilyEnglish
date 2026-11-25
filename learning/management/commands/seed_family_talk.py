from django.core.management.base import BaseCommand

from learning.family_talk import from_tuples
from learning.models import Lesson
from learning.seed.family_talk_levels import LEVELS
from learning.seed.family_talk_phonics import PHONICS
from learning.seed.family_talk_phonics_year import NEW, WEEK_TALK


class Command(BaseCommand):
    help = "Load the 'Talk at home' sentences (Me & Sister … Me & Grandpa) into every kids' lesson."

    def handle(self, *args, **options):
        talk = {**PHONICS, **LEVELS}
        done, missing = 0, []
        for lesson in Lesson.objects.select_related("module"):
            rows = talk.get(lesson.title) or self._phonics_year(lesson, talk)
            if rows:
                lesson.family_talk = from_tuples(rows)
                lesson.save(update_fields=["family_talk"])
                done += 1
            else:
                missing.append(lesson.title)
        if options.get("verbosity", 1) == 0:
            return
        self.stdout.write(self.style.SUCCESS(f"Talk at home added to {done} lessons."))
        if missing:
            self.stdout.write(f"No sentences yet for: {', '.join(missing)} (use 'Make new sentences with AI').")

    @staticmethod
    def _phonics_year(lesson, talk):
        """Phonics Year days: two-sound days mix both sounds; weeks 8-36 share one set per week."""
        week = (lesson.module.plan or {}).get("week")
        if not week:
            return None
        if lesson.title.startswith("The sounds /"):
            a, b = lesson.title[len("The sounds "):].split(" and ")
            ra, rb = talk.get(f"The sound {a}"), talk.get(f"The sound {b}")
            return ra[:3] + rb[3:] if ra and rb else None
        key = WEEK_TALK.get(week)
        return NEW.get(key) or talk.get(key)
