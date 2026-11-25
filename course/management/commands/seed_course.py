from django.core.management.base import BaseCommand
from django.db import transaction

from course.content import all_lessons
from course.models import CourseLesson


class Command(BaseCommand):
    help = "Load or update the skill course (Listening, Speaking, Reading, Writing, Grammar)."

    @transaction.atomic
    def handle(self, *args, **options):
        made = updated = 0
        for skill, data in all_lessons():
            fields = {k: v for k, v in data.items() if k != "slug"}
            _, created = CourseLesson.objects.update_or_create(slug=data["slug"], defaults={"skill": skill, **fields})
            made += created
            updated += not created
        self.stdout.write(self.style.SUCCESS(
            f"Course ready: {made} new, {updated} updated, {CourseLesson.objects.count()} lessons in total."))
