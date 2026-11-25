import secrets
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
    Plan.MONTHLY: 299,
    Plan.HALF_YEAR: 1500,
    Plan.YEAR: 2500,
}

# Families outside Bangladesh pay in US dollars by card through SSLCommerz (it settles in taka).
PLAN_PRICES_USD = {
    Plan.FREE: 0,
    Plan.MONTHLY: 3,
    Plan.HALF_YEAR: 15,
    Plan.YEAR: 25,
}


def plan_price(plan, country):
    """(currency, amount) a family in this country pays for the plan."""
    if (country or "BD") == "BD":
        return "BDT", PLAN_PRICES_BDT[plan]
    return "USD", PLAN_PRICES_USD[plan]


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
    country = models.CharField(max_length=2, default="BD", help_text="ISO country code of the family, e.g. BD, IN, GB")
    created_at = models.DateTimeField(auto_now_add=True)
    # Refer & earn: a family that joins with this code gets a longer trial, and when it
    # first pays, the family that invited it gets free days.
    referral_code = models.CharField(max_length=12, unique=True, null=True, blank=True)
    referred_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name="referrals")
    referral_rewarded = models.BooleanField(default=False,
                                            help_text="The inviting family already got its reward")

    class Meta:
        verbose_name_plural = "families"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.new_referral_code()
        super().save(*args, **kwargs)

    @staticmethod
    def new_referral_code():
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O or 1/I to avoid mix-ups
        while True:
            code = "FE" + "".join(secrets.choice(alphabet) for _ in range(6))
            if not Family.objects.filter(referral_code=code).exists():
                return code

    def add_free_days(self, days):
        """Extend paid access by `days` from today or from the current end date."""
        start = max(self.paid_until or timezone.localdate(), timezone.localdate())
        self.paid_until = start + timedelta(days=days)
        if self.plan == Plan.FREE:
            self.plan = Plan.MONTHLY
        self.save()

    @property
    def trial_ends(self):
        days = settings.FREE_TRIAL_DAYS + (settings.REFERRAL_EXTRA_TRIAL_DAYS if self.referred_by_id else 0)
        return (self.created_at + timedelta(days=days)).date()

    @property
    def is_paid_active(self):
        return bool(self.paid_until and self.paid_until >= timezone.localdate())

    @property
    def is_free_country(self):
        """Families outside Bangladesh use everything free for now (FE_FREE_OUTSIDE_BD)."""
        return bool(settings.FE_FREE_OUTSIDE_BD and self.country and self.country != "BD")

    @property
    def has_full_access(self):
        """Paid plan active, free trial (invited families get a few days), or a family outside Bangladesh."""
        return self.is_paid_active or timezone.localdate() < self.trial_ends or self.is_free_country

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

    class Track(models.TextChoices):
        KID = "kid", "Young child (3–10 years) · 3 years"
        STUDENT = "student", "School student (class 6–10) · 2 years"
        IELTS = "ielts", "IELTS or university preparation · 2 years"
        ADULT = "adult", "Parent who studied at school or college · 1 year"
        ELDER = "elder", "Grandparent or adult who studied little · 3 years"

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
    # Leagues show only the avatar and this nickname to other families (never the real name).
    nickname = models.CharField(max_length=24, blank=True,
                                help_text="Shown to other families in leagues instead of the name")
    league = models.CharField(max_length=10, default="bronze")
    track = models.CharField(max_length=10, choices=Track.choices, blank=True,
                             help_text="Which full course this learner follows")

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

    AVATAR_WORDS = {"🦁": "Lion", "🐘": "Elephant", "🐯": "Tiger", "🐼": "Panda", "🦊": "Fox",
                    "🐢": "Turtle", "🦉": "Owl", "🐬": "Dolphin", "🐝": "Bee", "🌻": "Sunflower"}

    @property
    def public_name(self):
        """Safe name for leagues: the chosen nickname, or e.g. 'Tiger 482'."""
        if self.nickname:
            return self.nickname
        return f"{self.AVATAR_WORDS.get(self.avatar, 'Star')} {(self.pk or 0) * 37 % 900 + 100}"

    @property
    def course_track(self):
        """The chosen track, or a sensible guess from role and age."""
        if self.track:
            return self.track
        if self.role == self.Role.ADULT:
            return self.Track.ADULT
        return self.Track.STUDENT if (self.age or 0) >= 11 else self.Track.KID

    @property
    def is_young_child(self):
        return self.role == self.Role.CHILD and self.age is not None and self.age < 7


class PaymentRequest(models.Model):
    """A payment for a family plan.

    bKash / Nagad Send Money: the family types the TrxID and the admin confirms it.
    SSLCommerz (card, mobile banking, internet banking): confirmed automatically after the order validation API
    says VALID and the amount and currency match.
    """

    class Method(models.TextChoices):
        BKASH = "bkash", "bKash"
        NAGAD = "nagad", "Nagad"
        SSLCOMMERZ = "sslcommerz", "SSLCommerz (card / mobile banking)"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        REJECTED = "rejected", "Rejected"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="payments")
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    plan = models.CharField(max_length=20, choices=Plan.choices)
    amount_bdt = models.PositiveIntegerField()
    method = models.CharField(max_length=10, choices=Method.choices)
    transaction_id = models.CharField(max_length=40)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    # Online payments (SSLCommerz)
    currency = models.CharField(max_length=3, default="BDT")
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                 help_text="Amount in the payment currency (USD payments: dollars)")
    val_id = models.CharField(max_length=80, blank=True)
    bank_tran_id = models.CharField(max_length=80, blank=True)
    card_type = models.CharField(max_length=60, blank=True)
    note = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def display_amount(self):
        if self.currency == "USD" and self.amount is not None:
            return f"${self.amount:.2f}"
        return f"৳{self.amount_bdt}"

    def confirm(self):
        """Extend the family's access from today or from the current end date."""
        start = max(self.family.paid_until or timezone.localdate(), timezone.localdate())
        self.family.plan = self.plan
        self.family.paid_until = start + timedelta(days=PLAN_DAYS.get(self.plan, 0))
        self.family.save()
        self.status = self.Status.CONFIRMED
        self.save()
        # Refer & earn: the family that invited this one gets free days on its first payment,
        # and a commission on every confirmed payment (paid out by bKash after a hold period).
        fam = self.family
        if fam.referred_by_id and not fam.referral_rewarded:
            fam.referred_by.add_free_days(settings.REFERRAL_REWARD_DAYS)
            fam.referral_rewarded = True
            fam.save(update_fields=["referral_rewarded"])
        if fam.referred_by_id and settings.REFERRAL_COMMISSION_PCT > 0:
            ReferralEarning.objects.get_or_create(
                payment=self,
                defaults={"family": fam.referred_by, "from_family": fam,
                          "amount_bdt": self.amount_bdt * settings.REFERRAL_COMMISSION_PCT // 100,
                          "available_on": timezone.localdate() + timedelta(days=settings.REFERRAL_HOLD_DAYS)})


class ReferralEarning(models.Model):
    """Commission for the family that invited a paying family."""

    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="earnings")
    from_family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, related_name="+")
    payment = models.OneToOneField(PaymentRequest, on_delete=models.CASCADE, related_name="earning")
    amount_bdt = models.PositiveIntegerField()
    available_on = models.DateField()
    payout = models.ForeignKey("PayoutRequest", on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="earnings")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class PayoutRequest(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        PAID = "paid", "Paid"
        REJECTED = "rejected", "Rejected"

    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name="payouts")
    amount_bdt = models.PositiveIntegerField()
    bkash_number = models.CharField(max_length=14, help_text="Personal bKash number to receive the money")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.REQUESTED)
    note = models.CharField(max_length=200, blank=True, help_text="Admin note, e.g. bKash transaction ID")
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]


class UserDevice(models.Model):
    """A signed-in browser. Families can see their devices and sign out the others."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="devices")
    session_key = models.CharField(max_length=64, unique=True)
    label = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-last_seen"]
