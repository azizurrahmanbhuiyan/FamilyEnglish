from django.db import models
from django.utils import timezone

from core.models import Learner


class TalkProfile(models.Model):
    """What the learner told us in the setup questions. Shapes every talk lesson."""
    learner = models.OneToOneField(Learner, on_delete=models.CASCADE, related_name="talk_profile")
    level = models.PositiveSmallIntegerField(default=2, help_text="1 beginner … 5 advanced")
    reason = models.CharField(max_length=12, default="confidence")
    challenge = models.CharField(max_length=14, default="speaking")
    correct = models.CharField(max_length=8, default="big", help_text="always, big or end")
    interests = models.JSONField(default=list, blank=True, help_text="Category keys from talk.content.topics")
    voice = models.CharField(max_length=8, default="classic")
    speed = models.FloatField(default=1.0)
    daily_minutes = models.PositiveSmallIntegerField(default=10)
    done = models.BooleanField(default=False, help_text="Finished the setup questions")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Talk profile of {self.learner}"


class Article(models.Model):
    """A Read-and-talk article written by AI the first time someone opens a topic (then kept for everyone)."""
    slug = models.SlugField(max_length=40, unique=True)
    category = models.CharField(max_length=20)
    title = models.CharField(max_length=160)
    level = models.PositiveSmallIntegerField(default=3)
    body = models.TextField()
    questions = models.JSONField(default=list)
    words = models.JSONField(default=list, help_text="[[word, meaning], …]")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TalkSession(models.Model):
    class Kind(models.TextChoices):
        DAILY = "daily", "Daily talk"
        ROLEPLAY = "roleplay", "Role-play"
        CUSTOM = "custom", "My own role-play"
        ARTICLE = "article", "Read and talk"

    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="talk_sessions")
    kind = models.CharField(max_length=10, choices=Kind.choices)
    ref = models.CharField(max_length=60, blank=True, help_text="Role-play slug, article slug or topic key")
    title = models.CharField(max_length=160)
    setting = models.CharField(max_length=300, blank=True)
    persona = models.CharField(max_length=200, blank=True)
    goal = models.CharField(max_length=300, blank=True)
    messages = models.JSONField(default=list, help_text="[{role: assistant|user, content, conf?}]")
    script_step = models.PositiveSmallIntegerField(default=0, help_text="Next scripted line when AI is off")
    report = models.JSONField(null=True, blank=True)
    seconds = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.learner} · {self.title}"

    @property
    def user_turns(self):
        return [m for m in self.messages if m.get("role") == "user"]
