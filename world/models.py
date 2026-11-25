import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    """Country, mobile number and language of each account holder (parent or teacher)."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="world_profile")
    country = models.CharField(max_length=2, default="BD", help_text="ISO country code, e.g. BD, IN, GB")
    phone = models.CharField(max_length=20, blank=True, db_index=True, help_text="Full number with dial code, e.g. +8801712345678")
    language = models.CharField(max_length=12, default="en")
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.country} {self.phone}"


def profile_for(user):
    p, _ = Profile.objects.get_or_create(user=user)
    return p


class OneTimeCode(models.Model):
    """A 6-digit sign-in code sent by email or SMS. Only a hash of the code is stored."""

    class Purpose(models.TextChoices):
        SIGNUP = "signup", "Confirm sign-up"
        LOGIN = "login", "Sign in with a code"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="one_time_codes")
    purpose = models.CharField(max_length=10, choices=Purpose.choices)
    sent_to = models.CharField(max_length=200, help_text="Where it was sent (shown masked)")
    code_hash = models.CharField(max_length=128)
    attempts = models.PositiveSmallIntegerField(default=0)
    used = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    MAX_ATTEMPTS = 5
    LIFETIME = timedelta(minutes=10)

    class Meta:
        ordering = ["-created_at"]

    @classmethod
    def issue(cls, user, purpose, sent_to):
        code = f"{secrets.randbelow(1_000_000):06d}"
        cls.objects.filter(user=user, purpose=purpose, used=False).update(used=True)
        otp = cls.objects.create(user=user, purpose=purpose, sent_to=sent_to[:200], code_hash=make_password(code),
                                 expires_at=timezone.now() + cls.LIFETIME)
        return otp, code

    @property
    def is_live(self):
        return not self.used and self.attempts < self.MAX_ATTEMPTS and timezone.now() < self.expires_at

    def verify(self, code):
        if not self.is_live:
            return False
        self.attempts += 1
        ok = check_password((code or "").strip(), self.code_hash)
        if ok:
            self.used = True
        self.save(update_fields=["attempts", "used"])
        return ok


class UiText(models.Model):
    """One translated piece of text. Missing ones are saved as pending and translated later (AI or by hand)."""

    class Origin(models.TextChoices):
        AI = "ai", "AI"
        MANUAL = "manual", "Edited by hand"
        PENDING = "pending", "Waiting for translation"

    lang = models.CharField(max_length=12, db_index=True)
    key = models.CharField(max_length=40, help_text="Hash of the English text")
    source = models.TextField(help_text="English")
    text = models.TextField(blank=True, help_text="Translation (empty = not translated yet)")
    origin = models.CharField(max_length=8, choices=Origin.choices, default=Origin.PENDING)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["lang", "key"], name="uitext_once")]
        verbose_name = "Translation"

    @staticmethod
    def key_for(source):
        return hashlib.sha1(source.encode("utf-8")).hexdigest()

    def __str__(self):
        return f"[{self.lang}] {self.source[:50]}"
