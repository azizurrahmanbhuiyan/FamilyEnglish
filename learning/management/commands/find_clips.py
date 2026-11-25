from django.core.management.base import BaseCommand

from course.models import CourseLesson
from learning import clips
from learning.models import Lesson, TalkTopic, VideoClip


class Command(BaseCommand):
    help = ("Find 4-5 short on-topic YouTube clips (max 5 min each, 20 min per lesson) for lessons that "
            "don't have enough yet. Needs FE_YOUTUBE_API_KEY. Safe to run again: it continues where it stopped.")

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=30, help="Lessons per run (about 30 fit the free daily quota)")
        parser.add_argument("--only", choices=["kids", "course", "topics"], help="Only one kind of lesson")

    def handle(self, *args, limit=30, only=None, **options):
        groups = {"kids": Lesson.objects.select_related("module__level"), "course": CourseLesson.objects.all(),
                  "topics": TalkTopic.objects.all()}
        items = [i for name, qs in groups.items() if not only or only == name for i in qs]
        todo = [i for i in items
                if VideoClip.objects.for_item(i).exclude(status="rejected").count() < clips.MIN_CLIPS]
        self.stdout.write(f"{len(todo)} lessons need clips; doing up to {limit} now.")
        done = added = 0
        for item in todo[:limit]:
            try:
                n = clips.find_for(item)
            except clips.ClipError as exc:
                self.stdout.write(self.style.ERROR(str(exc)))
                self.stdout.write("Stopped. Run the command again tomorrow (the free quota resets daily).")
                break
            done += 1
            added += n
            self.stdout.write(f"  {item}: +{n} clip(s)")
        pending = VideoClip.objects.filter(status="pending").count()
        self.stdout.write(self.style.SUCCESS(f"Done: {done} lessons, {added} clips added. "
                                             f"{pending} clip(s) from other channels wait for approval in /admin."))
