"""XP ledger, daily goals, weekly leagues and the feature suggestion board."""

from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models import Family, Learner


class XPEvent(models.Model):
    """Every XP a learner earns. A key stops the same reward being given twice."""

    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name="xp_events")
    amount = models.IntegerField()
    reason = models.CharField(max_length=60)
    key = models.CharField(max_length=80, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("learner", "key")
        indexes = [models.Index(fields=["learner", "created_at"])]


class LearnerGoal(models.Model):
    learner = models.OneToOneField(Learner, on_delete=models.CASCADE, related_name="goal")
    xp = models.PositiveSmallIntegerField(default=30, help_text="XP per day")
    questions = models.PositiveSmallIntegerField(default=10, help_text="Questions answered per day")
    lessons = models.PositiveSmallIntegerField(default=1, help_text="Lessons finished per day")


class LeagueState(models.Model):
    """Singleton: the last week whose league results were settled."""

    last_settled = models.DateField(null=True, blank=True)


class FeatureIdea(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Suggested"
        PLANNED = "planned", "Planned"
        DONE = "done", "Done"

    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="ideas")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=120)
    details = models.TextField(blank=True, max_length=1000)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class FeatureVote(models.Model):
    idea = models.ForeignKey(FeatureIdea, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("idea", "user")
