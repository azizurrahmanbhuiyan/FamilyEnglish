import re
from datetime import timedelta

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from core.models import Family

from . import translate
from .data import countries, guess, normalise_phone
from .models import OneTimeCode, Profile, UiText

SIGNUP = {"first_name": "Amina", "email": "amina@example.com", "family_name": "", "relation": "",
          "password1": "very-safe-pass-9", "password2": "very-safe-pass-9"}


def code_from_mail():
    return re.search(r"\b(\d{6})\b", mail.outbox[-1].subject).group(1)


class PhoneTests(TestCase):
    def test_dial_codes_and_numbers(self):
        by = {c["iso"]: c for c in countries()}
        self.assertEqual(str(by["BD"]["dial"]), "880")
        self.assertEqual(str(by["IN"]["dial"]), "91")
        self.assertEqual(str(by["GB"]["dial"]), "44")
        self.assertGreater(len(by), 200)
        self.assertEqual(normalise_phone("01712-345678", "BD"), "+8801712345678")
        self.assertEqual(normalise_phone("1712345678", "BD"), "+8801712345678")
        self.assertEqual(normalise_phone("07400 123456", "GB"), "+447400123456")
        self.assertIsNone(normalise_phone("12", "BD"))
        self.assertIsNone(normalise_phone("not a number", "IN"))

    def test_guess_from_browser(self):
        rf = self.client.get("/").wsgi_request
        rf.META["HTTP_ACCEPT_LANGUAGE"] = "hi-IN,hi;q=0.9,en;q=0.8"
        self.assertEqual(guess(rf), ("IN", "hi"))
        rf.META["HTTP_ACCEPT_LANGUAGE"] = ""
        self.assertEqual(guess(rf), ("BD", "en"))


class SignupOtpTests(TestCase):
    def signup(self, **extra):
        data = {**SIGNUP, "language": "hi", "country": "IN", "phone": "98765 43210", **extra}
        return self.client.post(reverse("core:signup"), data)

    def test_signup_verify_creates_family_with_country(self):
        r = self.signup()
        self.assertRedirects(r, reverse("world:verify"))
        user = User.objects.get(email="amina@example.com")
        self.assertFalse(user.is_active)
        self.assertFalse(Family.objects.filter(owner=user).exists())
        p = Profile.objects.get(user=user)
        self.assertEqual((p.country, p.phone, p.language), ("IN", "+919876543210", "hi"))
        self.assertIn("FamilyEnglish", mail.outbox[-1].subject)
        self.assertNotIn(code_from_mail(), OneTimeCode.objects.get(user=user).code_hash)  # stored hashed
        r = self.client.post(reverse("world:verify"), {"code": code_from_mail()})
        self.assertRedirects(r, reverse("core:learner_add"))
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        fam = Family.objects.get(owner=user)
        self.assertEqual(fam.country, "IN")
        self.assertFalse(fam.is_free_country)  # paid everywhere by default
        self.assertTrue(Profile.objects.get(user=user).email_verified)

    def test_bad_phone_is_refused(self):
        r = self.signup(phone="123")
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.filter(email="amina@example.com").exists())

    def test_wrong_code_and_attempt_limit(self):
        self.signup()
        good = code_from_mail()
        bad = "000000" if good != "000000" else "111111"
        for _ in range(OneTimeCode.MAX_ATTEMPTS):
            r = self.client.post(reverse("world:verify"), {"code": bad})
            self.assertEqual(r.status_code, 200)
        r = self.client.post(reverse("world:verify"), {"code": good})
        self.assertEqual(r.status_code, 200)  # too many tries: even the right code stops working
        self.assertFalse(User.objects.get(email="amina@example.com").is_active)

    def test_expired_code(self):
        self.signup()
        OneTimeCode.objects.update(expires_at=timezone.now() - timedelta(seconds=1))
        r = self.client.post(reverse("world:verify"), {"code": code_from_mail()})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.get(email="amina@example.com").is_active)

    def test_resend_waits_a_minute(self):
        self.signup()
        n = len(mail.outbox)
        self.client.post(reverse("world:resend"))
        self.assertEqual(len(mail.outbox), n)  # too soon
        OneTimeCode.objects.update(created_at=timezone.now() - timedelta(minutes=2))
        self.client.post(reverse("world:resend"))
        self.assertEqual(len(mail.outbox), n + 1)
        r = self.client.post(reverse("world:verify"), {"code": code_from_mail()})
        self.assertRedirects(r, reverse("core:learner_add"))

    def test_unconfirmed_email_can_sign_up_again(self):
        self.signup()
        r = self.signup(first_name="Amina B")
        self.assertRedirects(r, reverse("world:verify"))
        self.assertEqual(User.objects.filter(email="amina@example.com").count(), 1)


class CodeLoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("amina", "amina@example.com", "very-safe-pass-9")
        Profile.objects.create(user=self.user, country="GB", phone="+447400123456", language="en")
        Family.objects.create(owner=self.user, name="A", country="GB")

    def test_login_by_email(self):
        r = self.client.post(reverse("world:login_code"), {"who": "Amina@Example.com", "country": "GB"})
        self.assertRedirects(r, reverse("world:verify"))
        r = self.client.post(reverse("world:verify"), {"code": code_from_mail()})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_login_by_mobile_number(self):
        self.client.post(reverse("world:login_code"), {"who": "07400 123456", "country": "GB"})
        self.client.post(reverse("world:verify"), {"code": code_from_mail()})
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_unknown_account_does_not_say_so(self):
        r = self.client.post(reverse("world:login_code"), {"who": "nobody@example.com", "country": "GB"}, follow=True)
        self.assertContains(r, "If an account exists")
        self.assertEqual(len(mail.outbox), 0)


class LanguageTests(TestCase):
    def setUp(self):
        translate.forget()

    def test_hand_written_hindi_and_rtl_arabic(self):
        self.client.get(reverse("growth:lang", args=["hi"]))
        r = self.client.get(reverse("core:login"))
        self.assertContains(r, 'lang="hi"')
        self.assertContains(r, "फिर से स्वागत है")
        self.client.get(reverse("growth:lang", args=["ar"]))
        r = self.client.get(reverse("core:login"))
        self.assertContains(r, 'dir="rtl"')
        self.assertContains(r, "مرحبًا بعودتك")

    def test_missing_text_is_queued_and_admin_text_wins(self):
        self.assertEqual(translate.text("A brand new sentence.", "sw"), "A brand new sentence.")
        row = UiText.objects.get(lang="sw", source="A brand new sentence.")
        self.assertEqual(row.text, "")
        row.text, row.origin = "Sentensi mpya kabisa.", UiText.Origin.MANUAL
        row.save()
        translate.forget("sw")
        self.assertEqual(translate.text("A brand new sentence.", "sw"), "Sentensi mpya kabisa.")
        self.assertEqual(translate.text("Hello", "bn", "হ্যালো"), "হ্যালো")
        self.assertEqual(translate.text("Hello", "en"), "Hello")

    def test_language_picker_lists_many(self):
        r = self.client.get(reverse("world:language"))
        self.assertContains(r, "हिन्दी")
        self.assertContains(r, "العربية")
        self.assertContains(r, "Kiswahili")

    def test_signup_page_has_dial_codes(self):
        r = self.client.get(reverse("core:signup"), HTTP_ACCEPT_LANGUAGE="en-GB")
        self.assertRegex(r.content.decode(), r'"dial": "?44"?')
        self.assertContains(r, "(+880)")

    def test_translate_ui_dry_run(self):
        from io import StringIO

        from django.core.management import call_command
        out = StringIO()
        call_command("translate_ui", "--lang", "sw", "--all", "--dry-run", stdout=out)
        self.assertRegex(out.getvalue(), r"Swahili \(sw\): \d{3,} to translate")


class PaidEverywhereTests(TestCase):
    def test_pricing_shows_plans_abroad(self):
        r = self.client.get(reverse("core:pricing"), HTTP_CF_IPCOUNTRY="AE")
        self.assertNotContains(r, "Free in your country for now")
        self.assertFalse(Family(name="x", country="AE").is_free_country)

    @override_settings(FE_FREE_OUTSIDE_BD=True)
    def test_switch_on_makes_abroad_free(self):
        self.assertTrue(Family(name="x", country="AE").is_free_country)
        with self.settings(FE_FREE_OUTSIDE_BD=True):
            r = self.client.get(reverse("core:pricing"), HTTP_CF_IPCOUNTRY="AE")
            self.assertContains(r, "Free in your country for now")
        r = self.client.get(reverse("core:pricing"), HTTP_CF_IPCOUNTRY="BD")
        self.assertNotContains(r, "Free in your country for now")


    def test_bd_family_still_pays(self):
        fam = Family(name="x", country="BD")
        self.assertFalse(fam.is_free_country)
