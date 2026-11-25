import re

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from core.models import Family, Learner

from .content import grammar as G
from .content import pronunciation as PR
from .content import sounds as S
from .content import stories as ST
from .models import Attempt


class ContentTests(TestCase):
    def test_lessons_are_complete_and_in_learning_order(self):
        stages = [s[0] for s in PR.STAGES]
        order = [stages.index(p["stage"]) for p in PR.LESSONS]
        self.assertEqual(order, sorted(order))  # sounds → endings → flow → accent
        self.assertEqual(len(PR.LESSONS), 22)
        for p in PR.LESSONS:
            self.assertTrue(p["hello"][1] and p["rule"][1], p["slug"])
            self.assertGreaterEqual(len(p["examples"]), 3, p["slug"])
            self.assertGreaterEqual(len(p["practice"]), 5, p["slug"])
            self.assertEqual(len(p["drill"]), 8, p["slug"])
            for kind, *rest in p["practice"]:
                if kind == "make":
                    re.compile(rest[1])
            for text, sound, bn, ipa in p["drill"]:
                self.assertTrue(text and bn and ipa, (p["slug"], text))
                self.assertIn(sound, S.SOUNDS, (p["slug"], sound))

    def test_stories_and_new_tenses(self):
        self.assertEqual(len(ST.STORIES), 7)
        for st in ST.STORIES:
            self.assertGreaterEqual(len(st["lines"]), 6)
            for en, bn, note in st["lines"]:
                self.assertTrue(en and bn and note, (st["slug"], en))
            self.assertEqual(len(st["quiz"]), 4)
        for slug in ("b1-present-perfect-continuous", "b2-past-perfect-continuous", "b2-tense-review"):
            self.assertIn(slug, G.BY_SLUG)


class PageTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("p@example.com", "p@example.com", "very-safe-pass-9")
        self.fam = Family.objects.create(owner=self.user, name="P")
        self.learner = Learner.objects.create(family=self.fam, name="Mina", role="child", birth_year=2015)
        self.client.force_login(self.user)
        s = self.client.session
        s["learner_id"] = self.learner.id
        s.save()

    def pay(self):
        from datetime import date
        Family.objects.filter(pk=self.fam.pk).update(paid_until=date(2099, 1, 1))

    def test_course_page_and_free_lessons(self):
        r = self.client.get(reverse("studio:pronunciation"))
        self.assertContains(r, "Your first pronunciation lesson")
        self.assertContains(r, "Intonation: the music of English")
        r = self.client.get(reverse("studio:pron_lesson", args=["pron-first-lesson"]))
        self.assertContains(r, "pron-first-lesson")
        self.assertContains(r, reverse("studio:pron_drill", args=["pron-first-lesson"]))
        r = self.client.get(reverse("studio:pron_drill", args=["pron-first-lesson"]))
        import json
        self.assertContains(r, json.dumps("ˈwɔːtə")[1:-1])
        r = self.client.get(reverse("studio:pron_lesson", args=["pron-schwa"]))
        self.assertEqual(r.status_code, 402)  # locked for free families

    def test_paid_family_practice_is_checked_and_recorded(self):
        self.pay()
        r = self.client.get(reverse("studio:pron_lesson", args=["pron-ed-endings"]))
        self.assertEqual(r.status_code, 200)
        r = self.client.post(reverse("studio:api_check"), {"lesson": "pron-ed-endings", "index": 0, "answer": "t"},
                             content_type="application/json")
        self.assertTrue(r.json()["ok"])
        r = self.client.post(reverse("studio:api_check"), {"lesson": "pron-ed-endings", "index": 4,
                             "answer": "I washed my hands and cleaned the table", "confidence": 0.9}, content_type="application/json")
        self.assertTrue(r.json()["ok"])
        kinds = set(Attempt.objects.filter(key="pron:pron-ed-endings").values_list("kind", flat=True))
        self.assertEqual(kinds, {"grammar", "repeat"})

    def test_stories(self):
        r = self.client.get(reverse("studio:stories"))
        self.assertContains(r, "The Tortoise and the Hare")
        r = self.client.get(reverse("studio:story", args=["lost-kite"]))
        self.assertContains(r, "Tara has a red kite.")
        self.assertContains(r, "flies‿it‿on")
        self.assertEqual(self.client.get(reverse("studio:story_shadow", args=["lost-kite"])).status_code, 200)
        r = self.client.get(reverse("studio:story_quiz", args=["lost-kite"]))
        self.assertContains(r, "story-lost-kite")
        r = self.client.post(reverse("studio:api_check"), {"lesson": "story-lost-kite", "index": 0, "answer": "red"},
                             content_type="application/json")
        self.assertTrue(r.json()["ok"])
        self.assertTrue(Attempt.objects.filter(key="story-quiz:lost-kite", kind="words").exists())

    def test_learn_and_sounds_link_to_the_course(self):
        self.assertContains(self.client.get(reverse("studio:learn")), reverse("studio:pronunciation"))
        self.assertContains(self.client.get(reverse("studio:sounds")), reverse("studio:pronunciation"))
