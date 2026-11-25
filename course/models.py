"""Skill course: Listening, Speaking, Reading, Writing and Grammar lessons in three
categories (Easy, Medium, Advanced), each with practice, mistake feedback and a self-test.
Also the AI level test that decides where each learner starts."""

from django.db import models
from django.utils import timezone

from core.models import Learner

from .qtypes import label as qtype_label


class Band(models.TextChoices):
    EASY = "easy", "Easy"
    MEDIUM = "medium", "Medium"
    ADVANCED = "advanced", "Advanced"


BAND_ORDER = [Band.EASY, Band.MEDIUM, Band.ADVANCED]
BAND_BN = {"easy": "সহজ", "medium": "মাঝারি", "advanced": "উচ্চতর"}


class CourseSkill(models.TextChoices):
    LISTENING = "listening", "Listening"
    SPEAKING = "speaking", "Speaking"
    READING = "reading", "Reading"
    WRITING = "writing", "Writing"
    GRAMMAR = "grammar", "Grammar"


COURSE_SKILLS = [s.value for s in CourseSkill]
SKILL_EMOJI = {"listening": "👂", "speaking": "🗣️", "reading": "📖", "writing": "✍️", "grammar": "🧩"}
SKILL_BN = {"listening": "শোনা", "speaking": "বলা", "reading": "পড়া", "writing": "লেখা", "grammar": "ব্যাকরণ"}
PASS_PERCENT = 60


def band_of_level(level):
    """Map the 0-8 family ladder to a course category."""
    if level is None:
        return Band.EASY
    return Band.EASY if level <= 3 else Band.MEDIUM if level <= 5 else Band.ADVANCED


class CourseLesson(models.Model):
    slug = models.SlugField(unique=True)
    skill = models.CharField(max_length=12, choices=CourseSkill.choices)
    band = models.CharField(max_length=10, choices=Band.choices)
    order = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=140)
    title_bn = models.CharField(max_length=160, blank=True)
    goal = models.CharField(max_length=200, blank=True)
    note_en = models.TextField(blank=True)
    note_bn = models.TextField(blank=True)
    guidance_bn = models.TextField(blank=True, help_text="Tip for Bangla speakers")
    examples = models.JSONField(default=list, blank=True)
    errors = models.JSONField(default=list, blank=True, help_text='[{"avoid","use","why"}]')
    passage = models.TextField(blank=True, help_text="Reading text, or listening script read aloud")
    passage_title = models.CharField(max_length=120, blank=True)
    video_query = models.CharField(max_length=200, blank=True)
    practice = models.JSONField(default=list, blank=True)
    selftest = models.JSONField(default=list, blank=True)
    minutes = models.PositiveSmallIntegerField(default=15)

    class Meta:
        ordering = ["skill", "band", "order"]

    def __str__(self):
        return f"{self.get_skill_display()} · {self.get_band_display()} {self.order}: {self.title}"

    @property
    def band_rank(self):
        return BAND_ORDER.index(self.band)

    @property
    def emoji(self):
        return SKILL_EMOJI.get(self.skill, "📘")

    @property
    def band_bn(self):
        return BAND_BN.get(self.band, "")

    @property
    def skill_bn(self):
        return SKILL_BN.get(self.skill, "")

    @property
    def video_url(self):
        from urllib.parse import quote_plus
        return "https://www.youtube.com/results?search_query=" + quote_plus(self.video_query or self.title)

    def qtypes(self):
        seen = []
        for it in self.practice + self.selftest:
            if it.get("qt") and it["qt"] not in seen:
                seen.append(it["qt"])
        return seen

    def qtype_labels(self):
        return [qtype_label(q) for q in self.qtypes()]


class CourseProgress(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="course_progress")
    lesson = models.ForeignKey(CourseLesson, on_delete=models.CASCADE, related_name="progress")
    practice_done = models.BooleanField(default=False)
    best_score = models.PositiveSmallIntegerField(default=0, help_text="Best self-test %")
    passed = models.BooleanField(default=False)
    stars = models.PositiveSmallIntegerField(default=0)
    attempts = models.PositiveSmallIntegerField(default=0)
    passed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("learner", "lesson")


class SelfTestAttempt(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="selftests")
    lesson = models.ForeignKey(CourseLesson, on_delete=models.CASCADE, related_name="attempts")
    score = models.PositiveSmallIntegerField(default=0)
    total = models.PositiveSmallIntegerField(default=0)
    percent = models.PositiveSmallIntegerField(default=0)
    passed = models.BooleanField(default=False)
    review = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]


class AnswerLog(models.Model):
    """Every checked answer: powers mistake history, weak spots and daily goals."""

    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="answers")
    lesson = models.ForeignKey(CourseLesson, on_delete=models.SET_NULL, null=True, blank=True)
    skill = models.CharField(max_length=12, blank=True)
    qtype = models.CharField(max_length=20, blank=True)
    source = models.CharField(max_length=12, default="practice", help_text="practice, selftest, drill, smart")
    correct = models.BooleanField(default=False)
    given = models.CharField(max_length=300, blank=True)
    expected = models.CharField(max_length=300, blank=True)
    ai_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["learner", "created_at"])]


class SmartTest(models.Model):
    """The AI level test. Answers are stored as the learner moves through the steps."""

    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="smart_tests")
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)
    step = models.PositiveSmallIntegerField(default=0)
    steps = models.JSONField(default=list, help_text="Remaining plan of steps, e.g. ['listening:1', …]")
    answers = models.JSONField(default=dict, blank=True)
    scores = models.JSONField(default=dict, blank=True, help_text="Raw scores per skill")
    levels = models.JSONField(default=dict, blank=True, help_text="Level 0-8 per skill")
    bands = models.JSONField(default=dict, blank=True, help_text="easy / medium / advanced per skill")
    report = models.JSONField(default=dict, blank=True, help_text="Summary, strengths, focus, tips")
    ai_used = models.BooleanField(default=False)

    class Meta:
        ordering = ["-started_at"]

    @property
    def done(self):
        return self.finished_at is not None

    def weakest(self):
        if not self.levels:
            return None
        return min(self.levels, key=lambda k: (self.levels[k], COURSE_SKILLS.index(k)))

    def overall(self):
        vals = [self.levels[k] for k in ("listening", "speaking", "reading", "writing") if k in self.levels]
        return round(sum(vals) / len(vals)) if vals else 0
