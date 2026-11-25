import json
import re
from datetime import date

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from core.models import Family, Learner

from . import engine as E
from .content import coaches as C
from .content import grammar as G
from .content import ielts as I
from .content import sounds as S
from .content import units as U
from .models import Attempt, Bookmark, Certificate, LessonDone


class ContentTests(TestCase):
    def test_counts(self):
        self.assertEqual(len(U.UNITS), 24)
        self.assertEqual(len(G.LESSONS), 41)
        self.assertEqual({lv for lv, *_ in G.LEVELS}, {g["level"] for g in G.LESSONS})
        self.assertGreaterEqual(len(C.COACHES), 15)
        self.assertEqual(len(I.TOPICS), 20)

    def test_units_are_complete(self):
        for u in U.UNITS:
            self.assertIn(u["grammar"], G.BY_SLUG)
            self.assertGreaterEqual(len(u["words"]), 6, u["slug"])
            self.assertGreaterEqual(len(u["phrases"]), 4, u["slug"])
            self.assertGreaterEqual(len(u["convo"]), 4, u["slug"])
            for w in u["words"]:
                p = U.parse_word(w)
                self.assertTrue(p["target"] and p["sound"] in S.SOUNDS and p["bn"], w)
            for _, sound, bn in u["phrases"]:
                self.assertIn(sound, S.SOUNDS)

    def test_grammar_practice_is_valid(self):
        for g in G.LESSONS:
            kinds = [p[0] for p in g["practice"]]
            self.assertIn("say", kinds, g["slug"])
            for p in g["practice"]:
                if p[0] == "make":
                    re.compile(p[2])
                if p[0] in ("fill", "fix"):
                    self.assertTrue(p[2], g["slug"])

    def test_ielts_courses(self):
        for band, slugs in I.COURSE.items():
            self.assertEqual(len(slugs), 12)
            self.assertTrue(all(s in I.BY_SLUG for s in slugs))
            self.assertEqual({I.BY_SLUG[s]["part"] for s in slugs}, {1, 2, 3})


class ScoringTests(TestCase):
    def test_similarity(self):
        self.assertEqual(E.similarity("Nice to meet you", "nice to meet you"), 100)
        self.assertGreater(E.similarity("Nice to meet you", "nice to meet"), 60)
        self.assertLess(E.similarity("family", "funny"), 30)
        self.assertEqual(E.similarity("hello", ""), 0)

    def test_word_marks(self):
        marks = E.word_marks("I can swim", "I can")
        self.assertEqual([m["ok"] for m in marks], [True, True, False])

    def test_typed_answers(self):
        self.assertTrue(E.check_typed(" An ", ["an"]))
        self.assertTrue(E.check_typed("She’s my friend.", ["she's my friend."]))
        self.assertFalse(E.check_typed("a", ["an"]))

    def test_analyse_speech(self):
        text = ("I live in Dhaka because my parents work here. However, I often visit my village, which is very peaceful. "
                "For example, last winter we caught fish and ate pitha. Although the city is busy, I like it.")
        r = E.analyse_speech(text, 25, 120, 40)
        self.assertGreater(r["wpm"], 60)
        self.assertGreaterEqual(len(r["linkers"]), 3)
        self.assertTrue(3 <= r["band"] <= 9)
        self.assertEqual(E.analyse_speech("", 10)["overall"], 0)

    def test_cefr_and_band(self):
        self.assertEqual(E.cefr(0), "A1")
        self.assertEqual(E.cefr(45), "B1")
        self.assertEqual(E.cefr(95), "C2")
        self.assertEqual(E.ielts_band(50), 5.5)
        self.assertEqual(E.ielts_band(100), 9.0)


class Base(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_curriculum", verbosity=0)
        call_command("seed_course", verbosity=0)
        call_command("seed_wordlists", verbosity=0)
        cls.user = get_user_model().objects.create_user("s@example.com", "s@example.com", "safe-pass-123")
        cls.family = Family.objects.create(name="Studio family", owner=cls.user)
        cls.kid = Learner.objects.create(family=cls.family, name="Mitu", role="child", birth_year=2015)

    def setUp(self):
        self.client.force_login(self.user)
        s = self.client.session
        s["learner_id"] = self.kid.pk
        s.save()

    def pay(self):
        Family.objects.filter(pk=self.family.pk).update(paid_until=date(2099, 1, 1))

    def api(self, name, data):
        return self.client.post(reverse(name), json.dumps(data), content_type="application/json")


class PageTests(Base):
    def test_free_family_pages(self):
        for name in ["studio:today", "studio:learn", "studio:coach", "studio:discover", "studio:progress", "studio:more",
                     "studio:grammar", "studio:ielts", "studio:sounds", "studio:my_words", "studio:badges", "studio:dictionary"]:
            r = self.client.get(reverse(name))
            self.assertEqual(r.status_code, 200, name)
            self.assertContains(r, "fe-tabbar")
        # the first unit and the first grammar lesson are free to try
        self.assertEqual(self.client.get(reverse("studio:unit_lesson", args=["hello", 1])).status_code, 200)
        self.assertEqual(self.client.get(reverse("studio:grammar_lesson", args=["a1-articles"])).status_code, 200)
        # the rest is in the family plan
        self.assertEqual(self.client.get(reverse("studio:unit_lesson", args=["family", 1])).status_code, 402)
        self.assertEqual(self.client.get(reverse("studio:grammar_lesson", args=["b1-passive"])).status_code, 402)
        self.assertEqual(self.client.get(reverse("studio:analyzer")).status_code, 402)

    def test_paid_lessons_render(self):
        self.pay()
        for u in U.UNITS[:3]:
            self.assertEqual(self.client.get(reverse("studio:unit", args=[u["slug"]])).status_code, 200)
            for n in (1, 2, 4, 5):
                r = self.client.get(reverse("studio:unit_lesson", args=[u["slug"], n]))
                self.assertEqual(r.status_code, 200)
                self.assertContains(r, "p-config")
            self.assertRedirects(self.client.get(reverse("studio:unit_lesson", args=[u["slug"], 3])),
                                 f"{reverse('studio:grammar_lesson', args=[u['grammar']])}?unit={u['slug']}")
        for g in G.LESSONS:
            self.assertEqual(self.client.get(reverse("studio:grammar_lesson", args=[g["slug"]])).status_code, 200)
        for lv, *_ in G.LEVELS:
            self.assertContains(self.client.get(reverse("studio:grammar"), {"level": lv}), "s-gcard")
        for c in C.COACHES:
            r = self.client.get(reverse("studio:coach_detail", args=[c["slug"]]))
            self.assertIn(r.status_code, (200, 302))
            for s in c["scenarios"]:
                self.assertEqual(self.client.get(reverse("studio:coach_play", args=[c["slug"], s["slug"]])).status_code, 200)
        for band in I.BANDS:
            self.assertEqual(self.client.get(reverse("studio:ielts_band", args=[band])).status_code, 200)
            topic = I.COURSE[band][-1]
            self.assertEqual(self.client.get(reverse("studio:ielts_unit", args=[band, topic])).status_code, 200)
            for n in (1, 2, 3):
                self.assertEqual(self.client.get(reverse("studio:ielts_lesson", args=[band, topic, n])).status_code, 200)
        self.assertEqual(self.client.get(reverse("studio:sound_drill", args=["θ"])).status_code, 200)
        self.assertEqual(self.client.get(reverse("studio:analyzer"), {"p": "2"}).status_code, 200)
        r = self.client.post(reverse("studio:rehearse"), {"text": "Good morning everyone. Today I will talk about my village."})
        self.assertContains(r, "Good morning everyone.")

    def test_dictionary(self):
        r = self.client.get(reverse("studio:dictionary"), {"q": "water"})
        self.assertContains(r, "water")


class ApiTests(Base):
    def setUp(self):
        super().setUp()
        self.pay()

    def test_attempt_and_finish(self):
        r = self.api("studio:api_attempt", {"kind": "repeat", "key": "unit:hello:1", "target": "thank you", "said": "thank you", "confidence": .9})
        self.assertGreaterEqual(r.json()["score"], 90)
        self.assertTrue(all(m["ok"] for m in r.json()["marks"]))
        r = self.api("studio:api_finish", {"key": "unit:hello:1", "title": "Hello", "score": 95})
        self.assertTrue(r.json()["first"])
        self.assertEqual(r.json()["gems"], 5)
        r = self.api("studio:api_finish", {"key": "unit:hello:1", "title": "Hello", "score": 80})
        self.assertFalse(r.json()["first"])
        self.assertEqual(LessonDone.objects.get(learner=self.kid, key="unit:hello:1").score, 95)
        self.assertEqual(self.kid.xp_events.filter(key="studio:unit:hello:1").count(), 1)

    def test_free_answer_in_conversation(self):
        r = self.api("studio:api_attempt", {"kind": "convo", "key": "unit:family:4", "target": "There are five people in my family.",
                                            "said": "We are four people at home", "free": True})
        self.assertGreaterEqual(r.json()["score"], 55)

    def test_grammar_check(self):
        g = G.BY_SLUG["a1-articles"]
        r = self.api("studio:api_check", {"lesson": "a1-articles", "index": 0, "answer": "an"})
        self.assertTrue(r.json()["ok"])
        r = self.api("studio:api_check", {"lesson": "a1-articles", "index": 0, "answer": "a"})
        self.assertFalse(r.json()["ok"])
        self.assertIn("umbrella", r.json()["right"])
        make = next(i for i, p in enumerate(g["practice"]) if p[0] == "make")
        r = self.api("studio:api_check", {"lesson": "a1-articles", "index": make, "answer": "I bought a pen at the shop."})
        self.assertTrue(r.json()["ok"])
        self.assertEqual(Attempt.objects.filter(learner=self.kid, kind="grammar").count(), 3)

    def test_analyse(self):
        r = self.api("studio:api_analyse", {"key": "speech:1", "transcript": "I like my school because my teachers are kind and helpful.",
                                            "seconds": 6, "targetWpm": 110, "minWords": 10})
        self.assertIn("overall", r.json())
        self.assertEqual(Attempt.objects.get(learner=self.kid, kind="speech").wpm, r.json()["wpm"])

    def test_bookmark_toggle(self):
        self.assertTrue(self.api("studio:api_bookmark", {"text": "family", "ipa": "/ˈfæməli/"}).json()["saved"])
        self.assertEqual(Bookmark.objects.filter(learner=self.kid).count(), 1)
        self.assertContains(self.client.get(reverse("studio:my_words")), "family")
        self.assertEqual(self.client.get(reverse("studio:my_words"), {"practise": 1}).status_code, 200)
        self.assertFalse(self.api("studio:api_bookmark", {"text": "family"}).json()["saved"])

    def test_scores_journey_and_tasks(self):
        for s in (90, 80, 70):
            E.record(self.kid, "repeat", "unit:hello:1", "hello", "hello", s, 5)
        E.record(self.kid, "grammar", "grammar:a1-be", "x", "x", 50, 5)
        sc = E.scores(self.kid)
        self.assertEqual(sc["parts"][0]["score"], 80)
        self.assertIsNotNone(sc["overall"])
        self.assertIn(E.journey(self.kid, sc)["current"], [c[0] for c in E.CEFR])
        tasks = E.today_tasks(self.kid)
        self.assertEqual([t["n"] for t in tasks], [2, 1, 4])
        self.api("studio:api_finish", {"key": "unit:hello:2", "title": "Hello sounds", "score": 90})
        self.assertTrue(E.today_tasks(self.kid)[0]["done"])
        r = self.client.get(reverse("studio:progress"))
        self.assertContains(r, "<polygon")

    def test_certificate_for_a_grammar_level(self):
        for g in G.by_level("C"):
            E.finish(self.kid, E.grammar_key(g["slug"]), g["title"], 90)
        cert = Certificate.objects.get(learner=self.kid, code="grammar-c")
        r = self.client.get(reverse("studio:certificate", args=[cert.number]))
        self.assertContains(r, "Certificate of Achievement")
        self.assertContains(r, "Mitu")

    def test_buy_freeze(self):
        w = E.wallet(self.kid)
        w.gems = 25
        w.save()
        self.client.post(reverse("studio:buy_freeze"))
        w.refresh_from_db()
        self.assertEqual((w.gems, w.extra_freezes), (5, 1))
        from growth import engine as growth
        self.assertEqual(growth.streak_info(Learner.objects.get(pk=self.kid.pk))["freezes_left"], 4)


class ShortsTests(Base):
    def test_content_and_feed(self):
        from . import shorts as SH
        self.assertGreater(len(SH.animated()), 500)
        self.assertEqual(len({s["id"] for s in SH.animated()}), len(SH.animated()))
        items, more, total = SH.feed(self.kid, "food")
        self.assertTrue(items and more)
        self.assertTrue(all(s["topic"] == "food" for s in items))
        r = self.client.get(reverse("studio:api_shorts"), {"t": "grammar", "o": 12})
        self.assertEqual(len(r.json()["items"]), 12)
        first = SH.animated()[0]["id"]
        r = self.client.get(reverse("studio:api_shorts"), {"s": first})
        self.assertEqual(r.json()["items"][0]["id"], first)
        self.assertContains(self.client.get(reverse("studio:shorts"), {"t": "ielts"}), "sh-feed")
        self.assertContains(self.client.get(reverse("studio:discover")), "sh-tile")

    def test_say_back_scores_and_free_limit(self):
        from . import shorts as SH
        pool = SH.animated()
        r = self.api("studio:api_short_try", {"id": pool[0]["id"], "said": pool[0]["line"], "confidence": .9})
        self.assertGreaterEqual(r.json()["score"], 90)
        self.assertEqual(r.json()["xp"], 5)
        self.assertEqual(self.api("studio:api_short_try", {"id": pool[0]["id"], "said": pool[0]["line"]}).json()["xp"], 0)
        for s in pool[1:5]:
            self.api("studio:api_short_try", {"id": s["id"], "said": "hello"})
        self.assertTrue(self.api("studio:api_short_try", {"id": pool[6]["id"], "said": "x"}).json().get("locked"))
        # a short already tried today can be tried again
        self.assertIn("score", self.api("studio:api_short_try", {"id": pool[1]["id"], "said": pool[1]["line"]}).json())
        self.pay()
        self.assertIn("score", self.api("studio:api_short_try", {"id": pool[7]["id"], "said": "x"}).json())

    def test_real_video_short(self):
        from learning.models import VideoClip
        clip = VideoClip.objects.create(youtube_id="abcdefghijk", start=10, end=30, title="At the station",
                                        say_line="Which platform does the train leave from?")
        r = self.client.get(reverse("studio:api_shorts"), {"t": "videos"})
        self.assertEqual(r.json()["items"][0]["youtube"], "abcdefghijk")
        r = self.api("studio:api_short_try", {"id": f"v.{clip.pk}", "said": "which platform does the train leave from"})
        self.assertGreaterEqual(r.json()["score"], 90)
