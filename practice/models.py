"""Practice tools: level checks, skill practice, speaking, writing, AI tutor,
vocabulary flashcards, tutorials and support tickets."""

from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import Family, Learner

# ---------------------------------------------------------------- vocabulary

# Leitner boxes: a right answer moves a card up a box, a wrong one back to box 1.
BOX_DAYS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}
LEARNED_BOX = 3


class VocabDeck(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=80)
    title_bn = models.CharField(max_length=120, blank=True)
    emoji = models.CharField(max_length=8, default="📘")
    level = models.PositiveSmallIntegerField(default=3, help_text="Level this deck suits (0-8)")
    order = models.PositiveSmallIntegerField(default=1)
    series = models.CharField(max_length=12, blank=True, db_index=True,
                              help_text="kids3000 or core7000 for the weekly word lists; blank for topic decks")
    week = models.PositiveSmallIntegerField(default=0)

    SERIES = {
        "kids3000": {"en": "3000 most frequent words", "bn": "সবচেয়ে বেশি ব্যবহৃত ৩০০০ শব্দ"},
        "core7000": {"en": "7000 most frequent words", "bn": "সবচেয়ে বেশি ব্যবহৃত ৭০০০ শব্দ"},
    }

    class Meta:
        ordering = ["level", "order"]

    def __str__(self):
        return self.title

    @property
    def band(self):
        if self.level <= 2:
            return "Beginner"
        return "Elementary" if self.level <= 4 else "Intermediate" if self.level <= 6 else "Advanced"


class VocabWord(models.Model):
    deck = models.ForeignKey(VocabDeck, on_delete=models.CASCADE, related_name="words")
    word = models.CharField(max_length=60)
    emoji = models.CharField(max_length=8, blank=True)
    meaning_bn = models.CharField(max_length=120, blank=True)
    example = models.CharField(max_length=200, blank=True)
    ipa = models.CharField(max_length=60, blank=True, help_text="British pronunciation, e.g. /ˈwɔːtə/")
    rank = models.PositiveSmallIntegerField(default=0, help_text="Frequency rank in its word list")
    pos = models.CharField(max_length=20, blank=True, help_text="Part of speech: noun, verb, adjective…")
    definition = models.CharField(max_length=200, blank=True, help_text="Simple English definition")
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["deck", "order"]

    def __str__(self):
        return self.word


class CardReview(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="card_reviews")
    word = models.ForeignKey(VocabWord, on_delete=models.CASCADE, related_name="reviews")
    box = models.PositiveSmallIntegerField(default=1)
    due = models.DateField(default=timezone.localdate)
    times_seen = models.PositiveIntegerField(default=0)
    times_right = models.PositiveIntegerField(default=0)
    last_grade = models.PositiveSmallIntegerField(default=2, help_text="0 forgot, 1 almost, 2 knew")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("learner", "word")

    FORGOT, ALMOST, KNEW = 0, 1, 2

    def rate(self, grade, today=None):
        """grade: 0 forgot (back to box 1), 1 almost (same box, see it again tomorrow), 2 knew it (box up).

        True/False are accepted too (knew it / forgot)."""
        if grade is True:
            grade = self.KNEW
        elif grade is False or grade is None:
            grade = self.FORGOT
        today = today or timezone.localdate()
        self.times_seen += 1
        if grade == self.KNEW:
            self.times_right += 1
            self.box = min(self.box + 1, 5)
            self.due = today + timedelta(days=BOX_DAYS[self.box])
        elif grade == self.ALMOST:
            self.due = today + timedelta(days=1)
        else:
            self.box = 1
            self.due = today + timedelta(days=BOX_DAYS[1])
        self.last_grade = grade
        self.save()


# ---------------------------------------------------------------- checks & practice

class SkillCheck(models.Model):
    """One scored test: a level check, skill practice round or dictation game."""

    class Kind(models.TextChoices):
        LEVEL_CHECK = "level_check", "Level check"
        PRACTICE = "practice", "Skill practice"
        DICTATION = "dictation", "Word dictation"
        TYPING = "typing", "Typing speed"
        WORDS = "words", "Word week"

    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="skill_checks")
    kind = models.CharField(max_length=12, choices=Kind.choices)
    skill = models.CharField(max_length=12)
    level = models.PositiveSmallIntegerField(null=True, blank=True,
                                             help_text="Level found (level checks only)")
    score = models.PositiveSmallIntegerField(default=0)
    total = models.PositiveSmallIntegerField(default=0)
    detail = models.CharField(max_length=40, blank=True, help_text="e.g. dictation difficulty")
    taken_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-taken_at"]

    @property
    def percent(self):
        return round(self.score * 100 / self.total) if self.total else 0


class SpeakingAttempt(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="speaking_attempts")
    target = models.CharField(max_length=300, help_text="Sentence to say, or the question asked")
    heard = models.TextField(blank=True, help_text="What the browser's speech recognition heard")
    score = models.PositiveSmallIntegerField(default=0, help_text="0-100")
    mode = models.CharField(max_length=10, default="repeat", help_text="repeat or answer")
    feedback = models.TextField(blank=True)
    ai_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]


class WritingAttempt(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="writing_attempts")
    prompt = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    corrected = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    ai_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]


class TutorMessage(models.Model):
    """Chat with the AI tutor. Parents can read their children's chats."""

    class Role(models.TextChoices):
        USER = "user", "Learner"
        ASSISTANT = "assistant", "Tutor"

    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="tutor_messages")
    role = models.CharField(max_length=10, choices=Role.choices)
    text = models.TextField()
    ai_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at", "id"]


# ---------------------------------------------------------------- help

class Tutorial(models.Model):
    order = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=120)
    title_bn = models.CharField(max_length=160, blank=True)
    group = models.CharField(max_length=40, default="Getting started")
    summary = models.CharField(max_length=240)
    steps_bn = models.TextField(help_text="One step per line, in Bangla")
    youtube_id = models.CharField(max_length=20, blank=True,
                                  help_text="Your own recorded walkthrough; leave blank until ready")
    minutes = models.PositiveSmallIntegerField(default=2)
    link_name = models.CharField(max_length=60, blank=True,
                                 help_text="URL name of the page this tutorial is about")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"

    def step_list(self):
        return [s.strip() for s in self.steps_bn.splitlines() if s.strip()]

    @property
    def embed_url(self):
        if not self.youtube_id:
            return ""
        return f"https://www.youtube-nocookie.com/embed/{self.youtube_id}?rel=0&modestbranding=1"


class SupportTicket(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Active"
        ANSWERED = "answered", "Resolved"
        CLOSED = "closed", "Closed"

    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=120)
    message = models.TextField()
    reply = models.TextField(blank=True)
    attachment = models.FileField(upload_to="support/%Y/%m/", blank=True,
                                  help_text="Optional screenshot (PNG/JPG, up to 3 MB)")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject
