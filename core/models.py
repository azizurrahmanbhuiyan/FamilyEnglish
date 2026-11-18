from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone


class Plan(models.TextChoices):
    FREE = "free", "Free"
    MONTHLY = "monthly", "Family Monthly"
    HALF_YEAR = "half_year", "Family 6 months"
    YEAR = "year", "Family 12 months"


PLAN_PRICES_BDT = {
    Plan.FREE: 0,
    Plan.MONTHLY: 199,
    Plan.HALF_YEAR: 999,
    Plan.YEAR: 1799,
}

PLAN_DAYS = {
    Plan.MONTHLY: 30,
    Plan.HALF_YEAR: 182,
    Plan.YEAR: 365,
}


class Family(models.Model):
    """One family account. Any adult (parent, grandparent, elder) can own it."""

    name = models.CharField(max_length=120, help_text="e.g. Rahman family")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_families"
    )
    plan = models.CharField(max_length=20, choices=Plan.choices, default=Plan.FREE)
    paid_until = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "families"

    def __str__(self):
        return self.name

    @property
    def trial_ends(self):
        return (self.created_at + timedelta(days=settings.FREE_TRIAL_DAYS)).date()

    @property
    def is_paid_active(self):
        return bool(self.paid_until and self.paid_until >= timezone.localdate())

    @property
    def has_full_access(self):
        """Paid plan active, or still inside the free trial."""
        return self.is_paid_active or timezone.localdate() <= self.trial_ends

    def managers(self):
        """Owner plus any co-managers (e.g. the other parent or a grandparent)."""
        ids = [self.owner_id] + list(self.memberships.values_list("user_id", flat=True))
        return type(self.owner).objects.filter(id__in=ids)

    def can_manage(self, user):
        return user.is_authenticated and (
            user.id == self.owner_id or self.memberships.filter(user=user).exists()
        )


class FamilyManager(models.Model):
    """A second adult who can manage the family account."""

    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="family_memberships")
    relation = models.CharField(max_length=40, blank=True, help_text="e.g. Mother, Grandfather")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("family", "user")


class Learner(models.Model):
    """A learner profile inside a family. Children need no email, phone or photo."""

    class Role(models.TextChoices):
        CHILD = "child", "Child"
        ADULT = "adult", "Adult / parent / elder"

    AVATARS = ["🦁", "🐘", "🐯", "🐼", "🦊", "🐢", "🦉", "🐬", "🐝", "🌻"]

    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="learners")
    name = models.CharField(max_length=40, help_text="First name or nickname")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CHILD)
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    avatar = models.CharField(max_length=8, default="🦁")
    pin_hash = models.CharField(max_length=128, blank=True,
                                help_text="Optional 4-digit picture code for the profile")
    daily_limit_minutes = models.PositiveSmallIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.avatar} {self.name}"

    def set_pin(self, raw_pin):
        self.pin_hash = make_password(raw_pin) if raw_pin else ""

    def check_pin(self, raw_pin):
        return not self.pin_hash or check_password(raw_pin or "", self.pin_hash)

    @property
    def age(self):
        if not self.birth_year:
            return None
        return timezone.localdate().year - self.birth_year

    @property
    def is_young_child(self):
        return self.role == self.Role.CHILD and self.age is not None and self.age < 7


class PaymentRequest(models.Model):
    """A manual bKash / Nagad payment the admin confirms. Replace with a gateway later."""

    class Method(models.TextChoices):
        BKASH = "bkash", "bKash"
        NAGAD = "nagad", "Nagad"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        REJECTED = "rejected", "Rejected"

    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="payments")
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    plan = models.CharField(max_length=20, choices=Plan.choices)
    amount_bdt = models.PositiveIntegerField()
    method = models.CharField(max_length=10, choices=Method.choices)
    transaction_id = models.CharField(max_length=40)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def confirm(self):
        """Extend the family's access from today or from the current end date."""
        start = max(self.family.paid_until or timezone.localdate(), timezone.localdate())
        self.family.plan = self.plan
        self.family.paid_until = start + timedelta(days=PLAN_DAYS.get(self.plan, 0))
        self.family.save()
        self.status = self.Status.CONFIRMED
        self.save()
