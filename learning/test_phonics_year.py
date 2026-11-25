from datetime import date

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from core.access import can_open_lesson
from core.models import Family, Learner

from .models import Lesson, Progress
from .phonics_year import build
from .seed.phonics_year import STORIES, TRICKY


class PhonicsYearTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_curriculum", verbosity=0)
        cls.user = get_user_model().objects.create_user("py@x.com", "py@x.com", "safe-pass-123")
        cls.family = Family.objects.create(name="Class 1", owner=cls.user)
        cls.kid = Learner.objects.create(family=cls.family, name="Rafi", role="child", birth_year=2020)
        cls.kid2 = Learner.objects.create(family=cls.family, name="Mina", role="child", birth_year=2021)

    def setUp(self):
        self.client.force_login(self.user)
        s = self.client.session
        s["learner_id"] = self.kid.pk
        s.save()

    def test_content_is_complete(self):
        weeks = list(build())
        self.assertEqual(len(weeks), 36)
        self.assertEqual(len(STORIES), 42)
        self.assertEqual(sum(len(v) for v in TRICKY.values()), 60)
        for wk, prepare, days in weeks:
            self.assertEqual(len(days), 5)
            self.assertTrue(prepare)
            for d in days:
                self.assertTrue(d["teacher"]["steps"], d["title"])
                self.assertTrue(d["note_bn"] and d["home_task_bn"], d["title"])
                self.assertGreaterEqual(len(d["items"]), 2, d["title"])
        checks = [d for _, _, days in weeks for d in days if d["kind"].startswith("assess")]
        self.assertEqual(len(checks), 10)

    def test_first_two_weeks_free_rest_paid(self):
        week = lambda n: Lesson.objects.filter(module__plan__week=n).first()
        self.assertTrue(can_open_lesson(self.family, week(1)))
        self.assertTrue(can_open_lesson(self.family, week(2)))
        self.assertFalse(can_open_lesson(self.family, week(3)))
        self.assertEqual(self.client.get(reverse("learning:lesson", args=[week(3).pk])).status_code, 402)
        self.assertEqual(self.client.get(reverse("learning:phonics_week", args=[3])).status_code, 402)
        Family.objects.filter(pk=self.family.pk).update(paid_until=date(2099, 1, 1))
        self.assertEqual(self.client.get(reverse("learning:phonics_week", args=[36])).status_code, 200)

    def test_pages(self):
        first = Lesson.objects.get(module__plan__week=1, order=1)
        r = self.client.get(reverse("learning:lesson", args=[first.pk]) + "?view=parent")
        self.assertContains(r, "guide")
        self.assertContains(r, 'data-guide="bn"')
        self.assertContains(r, "tiny hole")
        self.assertContains(r, "সাইকেলের চাকায়")
        self.assertNotContains(self.client.get(reverse("learning:lesson", args=[first.pk]) + "?view=kid"), "tiny hole")
        r = self.client.get(reverse("learning:phonics_week", args=[1]))
        self.assertContains(r, "Print the week")
        self.assertContains(r, "Monday")
        check = Lesson.objects.get(module__plan__week=12, order=3)
        Progress.objects.create(learner=self.kid2, lesson=check, score=75, stars=2)
        r = self.client.get(reverse("learning:phonics_year"))
        self.assertContains(r, "Term 3")
        self.assertContains(r, "Mina")
        self.assertContains(r, "75%")
