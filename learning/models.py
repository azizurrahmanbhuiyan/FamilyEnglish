from django.db import models
from django.utils import timezone

from core.models import Learner


class Skill(models.TextChoices):
    LISTENING = "listening", "Listening"
    SPEAKING = "speaking", "Speaking"
    READING = "reading", "Reading"
    WRITING = "writing", "Writing"
    PHONICS = "phonics", "Phonics"


SKILLS_4 = [Skill.LISTENING, Skill.SPEAKING, Skill.READING, Skill.WRITING]


class Level(models.Model):
    """The 9-level family ladder (0-8)."""

    number = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=60)
    name_bn = models.CharField(max_length=80, blank=True)
    matches = models.CharField(max_length=120, help_text="e.g. Pre A1 Starters")
    typical_learner = models.CharField(max_length=120, blank=True)
    can_do = models.TextField(help_text="What learners can do at the end of the level")
    planned_lessons = models.PositiveSmallIntegerField(default=40)
    colour = models.CharField(max_length=20, default="#e11d48")

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Level {self.number} · {self.name}"


class Module(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="modules")
    order = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=120)
    title_bn = models.CharField(max_length=160, blank=True)
    summary_bn = models.TextField(blank=True)

    class Meta:
        ordering = ["level__number", "order"]

    def __str__(self):
        return f"L{self.level.number}.{self.order} {self.title}"


class Lesson(models.Model):
    class Activity(models.TextChoices):
        SOUND_TAP = "sound_tap", "Tap the sound"
        DICTATION = "dictation", "Dictation (hear and type)"
        QUIZ = "quiz", "Quiz"
        SPEAK = "speak", "Say it and record"

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")
    order = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=140)
    skill = models.CharField(max_length=12, choices=Skill.choices, default=Skill.PHONICS)
    minutes = models.PositiveSmallIntegerField(default=15)
    focus = models.CharField(max_length=60, blank=True, help_text="e.g. the sound /s/")
    action_hint = models.CharField(max_length=200, blank=True,
                                   help_text="Our own action for the sound (not copied from any programme)")
    note_bn = models.TextField(help_text="Bangla note for parents (Markdown-lite: blank lines = paragraphs)")
    note_en = models.TextField(blank=True, help_text="Short English note for the child view")
    home_task_bn = models.TextField(help_text="'Use it at home' task in Bangla")
    home_task_en = models.TextField(blank=True)
    activity = models.CharField(max_length=12, choices=Activity.choices, default=Activity.DICTATION)

    class Meta:
        ordering = ["module__level__number", "module__order", "order"]

    def __str__(self):
        return self.title

    @property
    def level(self):
        return self.module.level

    def sequence_key(self):
        return (self.module.level.number, self.module.order, self.order)


class LessonVideo(models.Model):
    """A free video from an official channel. Store the YouTube ID; we never re-host videos."""

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="videos")
    order = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=200)
    channel = models.CharField(max_length=80)
    youtube_id = models.CharField(max_length=20, blank=True,
                                  help_text="Leave blank until checked; the page then shows a search link")
    search_query = models.CharField(max_length=200, blank=True,
                                    help_text="Used to build a YouTube search link when no ID is set")
    why_watch_bn = models.CharField(max_length=240, blank=True)
    minutes = models.PositiveSmallIntegerField(default=5)
    made_for_kids = models.BooleanField(default=True,
                                        help_text="Made-for-kids videos must be embedded with tracking off")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        if not self.youtube_id:
            return ""
        # youtube-nocookie + no related videos from other channels + no autoplay
        return (f"https://www.youtube-nocookie.com/embed/{self.youtube_id}"
                "?rel=0&modestbranding=1&playsinline=1")

    @property
    def search_url(self):
        from urllib.parse import quote_plus
        return "https://www.youtube.com/results?search_query=" + quote_plus(
            self.search_query or f"{self.channel} {self.title}")


class PracticeItem(models.Model):
    """A word for dictation / tap-the-sound, or a quiz question."""

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="items")
    order = models.PositiveSmallIntegerField(default=1)
    prompt = models.CharField(max_length=200, help_text="Word to say, or question text")
    answer = models.CharField(max_length=120)
    choices = models.CharField(max_length=300, blank=True, help_text="Comma-separated options for quiz / tap")
    picture = models.CharField(max_length=8, blank=True, help_text="An emoji used as the picture")
    meaning_bn = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["order"]

    def choice_list(self):
        return [c.strip() for c in self.choices.split(",") if c.strip()]


class PlacementQuestion(models.Model):
    """Adaptive placement bank. Listening prompts are spoken by the browser (no audio files needed)."""

    skill = models.CharField(max_length=12, choices=Skill.choices)
    level = models.PositiveSmallIntegerField(help_text="Level this question checks (0-8)")
    prompt = models.CharField(max_length=300)
    spoken = models.CharField(max_length=300, blank=True, help_text="Text the browser reads aloud")
    picture = models.CharField(max_length=8, blank=True)
    choices = models.CharField(max_length=300)
    answer = models.CharField(max_length=120)

    class Meta:
        ordering = ["skill", "level", "id"]

    def choice_list(self):
        return [c.strip() for c in self.choices.split(",") if c.strip()]

    def __str__(self):
        return f"[{self.skill} L{self.level}] {self.prompt[:50]}"


class Placement(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="placements")
    taken_at = models.DateTimeField(default=timezone.now)
    listening = models.PositiveSmallIntegerField(default=0)
    speaking = models.PositiveSmallIntegerField(default=0)
    reading = models.PositiveSmallIntegerField(default=0)
    writing = models.PositiveSmallIntegerField(default=0)
    overall = models.PositiveSmallIntegerField(default=0)
    young_child_test = models.BooleanField(default=False)

    class Meta:
        ordering = ["-taken_at"]

    def skill_levels(self):
        return {s.value: getattr(self, s.value) for s in SKILLS_4}

    def weakest_skill(self):
        levels = self.skill_levels()
        return min(levels, key=levels.get)


class StudyPlan(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="plans")
    start_level = models.PositiveSmallIntegerField()
    target_level = models.PositiveSmallIntegerField()
    months = models.PositiveSmallIntegerField()
    days_per_week = models.PositiveSmallIntegerField(default=5)
    minutes_per_day = models.PositiveSmallIntegerField(default=20)
    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def progress(self):
        total = self.days.count()
        done = self.days.filter(status=PlanDay.Status.DONE).count()
        return done, total


class PlanDay(models.Model):
    class Status(models.TextChoices):
        TODO = "todo", "To do"
        DONE = "done", "Done"

    plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name="days")
    date = models.DateField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    kind = models.CharField(max_length=12, default="lesson",
                            help_text="lesson, review or family")
    status = models.CharField(max_length=6, choices=Status.choices, default=Status.TODO)

    class Meta:
        ordering = ["date", "id"]


class Progress(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(default=0)
    score = models.PositiveSmallIntegerField(default=0, help_text="Practice score in %")
    completed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("learner", "lesson")
        ordering = ["-completed_at"]
