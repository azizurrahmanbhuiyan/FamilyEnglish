import datetime as _dt

PAID_UNTIL = _dt.date.today() + _dt.timedelta(days=60)  # tests use a paying family unless they say otherwise
import json
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from core.models import Family, Learner
from growth.engine import totals

from .family_talk import MEMBER_KEYS, ai_generate
from .models import FamilyTalkSet, Lesson


class FamilyTalkTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_curriculum", verbosity=0)
        user = get_user_model().objects.create_user("p@example.com", "p@example.com", "safe-pass-123")
        cls.user = user
        cls.family = Family.objects.create(name="Khan family", owner=user, paid_until=PAID_UNTIL)
        cls.kid = Learner.objects.create(family=cls.family, name="Rafi", role="child", birth_year=2019)

    def setUp(self):
        self.client.force_login(self.user)
        s = self.client.session
        s["learner_id"] = self.kid.pk
        s.save()

    def test_every_kids_lesson_has_six_talks_of_two_lines(self):
        for lesson in Lesson.objects.all():
            self.assertEqual([t["who"] for t in lesson.family_talk], MEMBER_KEYS, lesson.title)
            for t in lesson.family_talk:
                self.assertTrue(t["me"] and t["them"] and t["me_bn"] and t["them_bn"], lesson.title)
                self.assertLessEqual(len(t["me"].split()), 12, t["me"])

    def test_lesson_page_shows_all_family_members(self):
        lesson = Lesson.objects.get(title="The sound /s/")
        r = self.client.get(reverse("learning:lesson", args=[lesson.pk]))
        for name in ["Sister", "Brother", "Mamma", "Daddy", "Grandma", "Grandpa"]:
            self.assertContains(r, f"&amp; {name}")
        self.assertContains(r, "Look, the sun is out!")

    def test_we_said_it_gives_xp_once(self):
        lesson = Lesson.objects.get(title="My family")
        url = reverse("learning:talk_said", args=[lesson.pk, "grandma"])
        self.client.post(url)
        self.client.post(url)
        self.assertEqual(totals(self.kid)["xp"], 5)
        r = self.client.get(reverse("learning:lesson", args=[lesson.pk]))
        self.assertContains(r, "✅ Said")

    def test_hub_and_dashboard(self):
        r = self.client.get(reverse("learning:talk_hub") + "?who=daddy&level=0")
        self.assertContains(r, "Daddy, can we play in the sand?")
        self.assertContains(self.client.get(reverse("learning:today")), "s family talk")

    def test_ai_button_needs_key(self):
        lesson = Lesson.objects.first()
        self.client.post(reverse("learning:talk_ai", args=[lesson.pk]))
        self.assertFalse(FamilyTalkSet.objects.exists())

    @override_settings(AI_API_KEY="test-key")
    def test_ai_makes_family_set_and_original_stays(self):
        lesson = Lesson.objects.get(title="The sounds /m/ and /d/")
        fake = json.dumps([{"who": w, "me": f"My {w} line.", "them": "Yes, my dear.", "me_bn": "আমার",
                            "them_bn": "হ্যাঁ"} for w in MEMBER_KEYS])
        with mock.patch("practice.ai.ask", return_value=fake):
            self.client.post(reverse("learning:talk_ai", args=[lesson.pk]))
        self.assertEqual(FamilyTalkSet.objects.get().learner, self.kid)
        page = self.client.get(reverse("learning:lesson", args=[lesson.pk]))
        self.assertContains(page, "My grandpa line.")
        original = self.client.get(reverse("learning:lesson", args=[lesson.pk]) + "?talk=original")
        self.assertContains(original, "My mango! Yum!")

    def test_ai_reply_must_cover_all_six(self):
        lesson = Lesson.objects.first()
        bad = json.dumps([{"who": "sister", "me": "Hi", "them": "Hello"}])
        with mock.patch("practice.ai.ask", return_value=bad):
            self.assertIsNone(ai_generate(lesson, self.kid))


class TalkTopicTests(FamilyTalkTests):
    def test_thirty_theme_lessons_with_words_and_six_talks(self):
        from .models import TalkTopic
        self.assertEqual(TalkTopic.objects.filter(group="daily").count(), 11)
        self.assertEqual(TalkTopic.objects.filter(group="study").count(), 13)
        self.assertEqual(TalkTopic.objects.filter(group="trip").count(), 6)
        for t in TalkTopic.objects.all():
            self.assertEqual(len(t.words), 8, t.slug)
            self.assertEqual([x["who"] for x in t.family_talk], MEMBER_KEYS, t.slug)

    def test_hub_tabs_and_topic_page(self):
        r = self.client.get(reverse("learning:talk_hub"))
        self.assertContains(r, "Good morning")
        self.assertContains(self.client.get(reverse("learning:talk_hub") + "?tab=trip"), "Trip to the sea beach")
        page = self.client.get(reverse("learning:talk_topic", args=["prayers"]))
        self.assertContains(page, "Apu, it&#x27;s time for Asr prayer.")
        self.assertContains(page, "জায়নামাজ")
        rhyme = self.client.get(reverse("learning:talk_topic", args=["rhymes"]))
        self.assertContains(rhyme, "Twinkle, twinkle, little star")

    def test_topic_said_xp_once_and_progress(self):
        url = reverse("learning:topic_said", args=["planets", "daddy"])
        self.client.post(url)
        self.client.post(url)
        self.assertEqual(totals(self.kid)["xp"], 5)
        self.assertContains(self.client.get(reverse("learning:talk_hub") + "?tab=study"), "1/6")

    @override_settings(AI_API_KEY="test-key")
    def test_topic_ai_set(self):
        fake = json.dumps([{"who": w, "me": f"Zoo line {w}.", "them": "OK!", "me_bn": "", "them_bn": ""} for w in MEMBER_KEYS])
        with mock.patch("practice.ai.ask", return_value=fake):
            self.client.post(reverse("learning:topic_ai", args=["zoo"]))
        self.assertContains(self.client.get(reverse("learning:talk_topic", args=["zoo"])), "Zoo line grandma.")
