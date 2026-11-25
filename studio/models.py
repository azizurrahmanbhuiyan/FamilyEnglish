"""Speaking studio: every spoken or typed try is an Attempt, which feeds the scores and history."""

from django.db import models
from django.utils import timezone

from core.models import Learner


class Attempt(models.Model):
    class Kind(models.TextChoices):
        REPEAT = "repeat", "Repeat after me"
        CONVO = "convo", "Scripted conversation"
        GRAMMAR = "grammar", "Grammar practice"
        SPEECH = "speech", "Speech analyzer"
        COACH = "coach", "Coach role-play"
        IELTS = "ielts", "IELTS speaking"
        LISTEN = "listen", "Listening"
        WORDS = "words", "Vocabulary"
        SHORT = "short", "Short video say-back"

    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="studio_attempts")
    kind = models.CharField(max_length=10, choices=Kind.choices)
    key = models.CharField(max_length=80, help_text="Lesson key, e.g. unit:family:2 or grammar:a1-articles")
    item = models.CharField(max_length=200, blank=True, help_text="The word, phrase or question practised")
    said = models.TextField(blank=True, help_text="What the learner said or typed")
    score = models.PositiveSmallIntegerField(default=0, help_text="0–100")
    seconds = models.PositiveIntegerField(default=0, help_text="Time spent")
    wpm = models.PositiveSmallIntegerField(default=0, help_text="Words per minute (speaking)")
    ai_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["learner", "kind", "created_at"]), models.Index(fields=["learner", "key"])]

    def __str__(self):
        return f"{self.learner} {self.kind} {self.key} {self.score}"


class LessonDone(models.Model):
    """A finished studio lesson (unit lesson, grammar lesson, coach scenario, IELTS lesson)."""
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="studio_done")
    key = models.CharField(max_length=80)
    title = models.CharField(max_length=160, blank=True)
    score = models.PositiveSmallIntegerField(default=0)
    finished_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-finished_at"]
        constraints = [models.UniqueConstraint(fields=["learner", "key"], name="studio_done_once")]


class Bookmark(models.Model):
    """'My Words': words and phrases a learner saved to practise again."""
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="bookmarks")
    text = models.CharField(max_length=120)
    ipa = models.CharField(max_length=80, blank=True)
    meaning_bn = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["learner", "text"], name="bookmark_once")]


class Wallet(models.Model):
    """Gems: earned for finished lessons and perfect days; spent on a streak freeze or skips."""
    learner = models.OneToOneField(Learner, on_delete=models.CASCADE, related_name="wallet")
    gems = models.PositiveIntegerField(default=0)
    earned = models.PositiveIntegerField(default=0)
    extra_freezes = models.PositiveSmallIntegerField(default=0, help_text="Streak freezes bought for freeze_month")
    freeze_month = models.CharField(max_length=7, blank=True, help_text="YYYY-MM the bought freezes belong to")


class Certificate(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="certificates")
    code = models.CharField(max_length=40, help_text="What it is for, e.g. grammar-a1 or cefr-b1")
    title = models.CharField(max_length=160)
    title_bn = models.CharField(max_length=200, blank=True)
    number = models.CharField(max_length=20, unique=True)
    issued_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-issued_at"]
        constraints = [models.UniqueConstraint(fields=["learner", "code"], name="certificate_once")]
