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
    plan = models.JSONField(default=dict, blank=True,
                            help_text="Phonics Year week: {week, term, goal, prepare: [...], tricky: [...]}")

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
    teacher = models.JSONField(default=dict, blank=True,
                               help_text="Parents' guide: {day, story, story_bn, steps: [{t, t_bn, min, do, do_bn}], words, sentences, tricky, text, kind}")
    family_talk = models.JSONField(
        default=list, blank=True,
        help_text='Talk at home: [{"who": "sister", "me": "...", "them": "...", "me_bn": "...", "them_bn": "..."}]')

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
    kind = models.CharField(max_length=10, default="levels",
                            help_text="levels = level ladder lessons; course = AI-test skill course; track = full programme")
    track = models.CharField(max_length=10, blank=True, help_text="kid, student, adult or elder (full programme)")

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
    course_lesson = models.ForeignKey("course.CourseLesson", on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey("learning.TalkTopic", on_delete=models.CASCADE, null=True, blank=True)
    deck = models.ForeignKey("practice.VocabDeck", on_delete=models.CASCADE, null=True, blank=True,
                             help_text="A week of the 3000/7000 word list")
    kind = models.CharField(max_length=12, default="lesson",
                            help_text="lesson, course, topic, review (repeat an earlier item) or family")
    stage = models.CharField(max_length=80, blank=True, help_text="Stage of a full programme, e.g. Year 1")

    XP = {"lesson": 50, "course": 60, "topic": 40, "words": 40, "review": 15, "family": 10}

    @property
    def item(self):
        return self.course_lesson or self.lesson or self.topic or self.deck

    @property
    def title(self):
        item = self.item
        if item and self.kind == "review":
            return f"Repeat: {item.title}"
        if item:
            return item.title
        return "Review day" if self.kind == "review" else "Family English day"

    @property
    def xp(self):
        return self.XP.get(self.kind, 10)
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


class TalkTopic(models.Model):
    """A 'Talk at home' theme lesson: daily life (good morning, prayers…) or a topic (animals, planets, trips…)."""

    class Group(models.TextChoices):
        DAILY = "daily", "Daily life"
        STUDY = "study", "Topics"
        TRIP = "trip", "Trips"

    slug = models.SlugField(unique=True)
    group = models.CharField(max_length=8, choices=Group.choices)
    order = models.PositiveSmallIntegerField(default=1)
    emoji = models.CharField(max_length=16, blank=True)
    title = models.CharField(max_length=120)
    title_bn = models.CharField(max_length=160, blank=True)
    intro_bn = models.TextField(blank=True)
    words = models.JSONField(default=list, blank=True, help_text='[{"word", "emoji", "bn"}]')
    rhyme = models.TextField(blank=True, help_text="Optional public-domain rhyme")
    rhyme_note = models.CharField(max_length=120, blank=True)
    family_talk = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["group", "order"]

    def __str__(self):
        return self.title


class FamilyTalkSet(models.Model):
    """New 'Talk at home' sentences a family asked the AI to make for one lesson (latest set is shown)."""

    family = models.ForeignKey("core.Family", on_delete=models.CASCADE, related_name="talk_sets")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="talk_sets", null=True, blank=True)
    topic = models.ForeignKey(TalkTopic, on_delete=models.CASCADE, related_name="talk_sets", null=True, blank=True)
    learner = models.ForeignKey("core.Learner", on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="talk_sets", help_text="Who asked (counts toward the daily AI limit)")
    data = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class VideoClipQuerySet(models.QuerySet):
    def for_item(self, item):
        return self.filter(**VideoClip.target_kwargs(item))

    def visible(self):
        return self.filter(status=VideoClip.Status.APPROVED)


class VideoClip(models.Model):
    """A short part of a YouTube video for one lesson: only seconds start..end are played.

    Max 5 minutes per clip and 20 minutes per lesson (see learning/clips.py)."""

    class Status(models.TextChoices):
        PENDING = "pending", "Waiting for approval"
        APPROVED = "approved", "Shown"
        REJECTED = "rejected", "Rejected"

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True, related_name="clips")
    course_lesson = models.ForeignKey("course.CourseLesson", on_delete=models.CASCADE, null=True, blank=True,
                                      related_name="clips")
    topic = models.ForeignKey(TalkTopic, on_delete=models.CASCADE, null=True, blank=True, related_name="clips")
    order = models.PositiveSmallIntegerField(default=1)
    youtube_id = models.CharField(max_length=20, help_text="Video ID or paste the full YouTube link")
    start = models.PositiveIntegerField(default=0, help_text="Start, in seconds")
    end = models.PositiveIntegerField(help_text="End, in seconds (at most 5 minutes after the start)")
    title = models.CharField(max_length=200, blank=True)
    channel = models.CharField(max_length=80, blank=True)
    part = models.CharField(max_length=120, blank=True, help_text="Chapter used, for long videos")
    source = models.CharField(max_length=8, default="manual")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.APPROVED)
    say_line = models.CharField(max_length=200, blank=True,
                                help_text="Short videos: the exact line spoken in this clip. Learners watch it, then say it back. "
                                          "Keep the clip under 60 seconds.")
    say_line_bn = models.CharField(max_length=240, blank=True, help_text="Bangla meaning of the line (optional)")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = VideoClipQuerySet.as_manager()

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.title or self.youtube_id} ({self.start_label}–{self.end_label})"

    @staticmethod
    def target_kwargs(item):
        from course.models import CourseLesson
        if isinstance(item, Lesson):
            return {"lesson": item}
        if isinstance(item, CourseLesson):
            return {"course_lesson": item}
        if isinstance(item, TalkTopic):
            return {"topic": item}
        raise ValueError("Unknown lesson type")

    @property
    def length(self):
        return max(0, self.end - self.start)

    @property
    def start_label(self):
        from .clips import fmt_time
        return fmt_time(self.start)

    @property
    def end_label(self):
        from .clips import fmt_time
        return fmt_time(self.end)

    @property
    def length_label(self):
        from .clips import fmt_time
        return fmt_time(self.length)

    @property
    def embed_url(self):
        # Only this part plays. youtube-nocookie, no autoplay, related videos only from the same channel.
        return (f"https://www.youtube-nocookie.com/embed/{self.youtube_id}?start={self.start}&end={self.end}"
                "&rel=0&modestbranding=1&playsinline=1")

    @property
    def thumb(self):
        return f"https://i.ytimg.com/vi/{self.youtube_id}/mqdefault.jpg"

    def clean(self):
        from django.core.exceptions import ValidationError
        from .clips import MAX_CLIP, MAX_TOTAL, youtube_id

        vid = youtube_id(self.youtube_id)
        if not vid:
            raise ValidationError({"youtube_id": "Paste a single YouTube video link or ID (not a playlist)."})
        self.youtube_id = vid
        targets = [x for x in (self.lesson_id, self.course_lesson_id, self.topic_id) if x]
        if len(targets) != 1:
            raise ValidationError("Choose exactly one lesson, course lesson or topic.")
        if self.end <= self.start:
            raise ValidationError({"end": "End must be after the start."})
        if self.end - self.start > MAX_CLIP:
            raise ValidationError({"end": "A clip can be at most 5 minutes long."})
        others = VideoClip.objects.filter(lesson_id=self.lesson_id, course_lesson_id=self.course_lesson_id,
                                          topic_id=self.topic_id).exclude(pk=self.pk).exclude(status="rejected")
        if sum(c.length for c in others) + self.length > MAX_TOTAL:
            raise ValidationError("All clips of a lesson together can be at most 20 minutes.")
