from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from core.models import Family

User = get_user_model()


@override_settings(FREE_TRIAL_DAYS=60, FREE_TRIAL_FROM="")
class FreeDaysTests(TestCase):
    """Every family gets everything free for 60 days, counted from its own sign-up."""

    def _family(self, joined_days_ago):
        u = User.objects.create_user(f"u{joined_days_ago}@example.com", password="x-pass-word-9")
        f = Family.objects.create(name="F", owner=u)
        Family.objects.filter(pk=f.pk).update(created_at=timezone.now() - timedelta(days=joined_days_ago))
        f.refresh_from_db()
        return f

    def test_sixty_days_from_sign_up(self):
        new, mid, old = self._family(0), self._family(59), self._family(61)
        self.assertEqual((new.trial_ends - timezone.localdate()).days, 60)
        self.assertTrue(new.has_full_access and mid.has_full_access)
        self.assertFalse(old.has_full_access)

    @override_settings(FREE_TRIAL_FROM="2026-11-26")
    def test_optional_start_date_for_older_families(self):
        self.assertEqual(self._family(400).trial_ends, date(2026, 11, 26) + timedelta(days=60))

    def test_pricing_and_signup_say_sixty_days_free(self):
        self.assertContains(self.client.get(reverse("core:pricing")), "first 60 days are free")
        self.assertContains(self.client.get(reverse("core:signup") + "?picked=1"), "first 60 days are free")
