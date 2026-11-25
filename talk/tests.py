import json
from datetime import date
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import Family, Learner

from . import engine as TE
from .content import roleplays as RP
from .content import topics as T
from .models import Article, TalkSession


class ContentTests(TestCase):
    def test_counts_and_unique_slugs(self):
        self.assertEqual(len(RP.ROLEPLAYS), 41)
        self.assertEqual(len(RP.BY_SLUG), 41)
        self.assertTrue(set(RP.POPULAR) <= set(RP.BY_SLUG) and RP.FREE <= set(RP.BY_SLUG))
        for r in RP.ROLEPLAYS:
            self.assertEqual(len(r["lines"]), 4, r["slug"])
            self.assertIn(r["category"], {k for k, *_ in RP.CATEGORIES})
        self.assertGreaterEqual(len(T.CATEGORIES), 18)
        seeds = [c["seed"]["slug"] for c in T.CATEGORIES]
        self.assertEqual(len(seeds), len(set(seeds)))
        for c in T.CATEGORIES:
            self.assertEqual(len(c["openers"]), 3)
            self.assertGreaterEqual(len(c["topics"]), 18)
            self.assertEqual(len(c["topics"]), len(set(c["topics"])))
            self.assertGreaterEqual(len(c["seed"]["body"].split()), 90, c["key"])
            self.assertEqual(len(c["seed"]["questions"]), 3)
        self.assertEqual(T.topic("travel-t1")[1], T.BY_KEY["travel"]["topics"][0])
        self.assertEqual(T.topic("travel-t99"), (None, None))
        self.assertGreaterEqual(sum(len(c["topics"]) for c in T.CATEGORIES), 400)
        titles = " ".join(t.lower() for c in T.CATEGORIES for t in c["topics"])
        for banned in ("bullfight", "gangster", "crime", "conspiracy", "cocktail", "mixology", "political", "ptsd", "evil", "haunted", "armstrong"):
            self.assertNotIn(banned, titles)


@override_settings(AI_API_KEY="")
class TalkWebTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("t@example.com", "t@example.com", "safe-pass-123")
        cls.family = Family.objects.create(name="Talk family", owner=cls.user)
        cls.kid = Learner.objects.create(family=cls.family, name="Rafi", role="child", birth_year=2014)

    def setUp(self):
        self.client.force_login(self.user)
        s = self.client.session
        s["learner_id"] = self.kid.pk
        s.save()

    def pay(self):
        Family.objects.filter(pk=self.family.pk).update(paid_until=date(2099, 1, 1))

    def post_json(self, name, pk, data=None):
        return self.client.post(reverse(name, args=[pk]), json.dumps(data or {}), content_type="application/json")

    def setup_profile(self):
        return self.client.post(reverse("talk:setup"), {"level": "3", "reason": "career", "challenge": "grammar", "correct": "always",
                                                        "interests": ["travel", "food", "pets", "nope"], "voice": "warm",
                                                        "speed": "0.8", "daily_minutes": "15"})

    def test_setup_first_then_home(self):
        self.assertRedirects(self.client.get(reverse("talk:home")), reverse("talk:setup"))
        self.assertEqual(self.client.get(reverse("talk:setup")).status_code, 200)
        self.assertRedirects(self.setup_profile(), reverse("talk:home"))
        p = TE.profile(self.kid)
        self.assertEqual((p.level, p.reason, p.correct, p.voice, p.speed, p.daily_minutes), (3, "career", "always", "warm", 0.8, 15))
        self.assertEqual(p.interests, ["travel", "food", "pets"])
        r = self.client.get(reverse("talk:home"))
        self.assertContains(r, "Daily talk")
        self.assertContains(r, "Job interview")  # career → work role-plays first

    def test_daily_talk_without_ai_and_report(self):
        self.setup_profile()
        r = self.client.post(reverse("talk:go", args=["daily"]))
        s = TalkSession.objects.get(learner=self.kid)
        self.assertRedirects(r, reverse("talk:chat", args=[s.pk]))
        self.assertContains(self.client.get(reverse("talk:chat", args=[s.pk])), "t-config")
        self.assertIn("Rafi", s.messages[0]["content"])
        d = self.post_json("talk:api_reply", s.pk, {"text": "I love travelling to Sylhet because the tea gardens are beautiful", "confidence": .9, "seconds": 6}).json()
        self.assertTrue(d["reply"].startswith("That's interesting!"))
        self.assertIn("I think", self.post_json("talk:api_hint", s.pk).json()["hint"])
        self.assertIsNone(self.post_json("talk:api_translate", s.pk, {"text": "Hello"}).json()["text"])
        url = self.post_json("talk:api_finish", s.pk).json()["url"]
        r = self.client.get(url)
        self.assertContains(r, "New words you used")
        rep = TalkSession.objects.get(pk=s.pk).report
        self.assertIn("gardens", rep["new_words"])
        self.assertEqual(rep["pronunciation"], 90)
        self.assertIsNone(rep["grammar"])
        self.assertFalse(rep["ai"])
        # free: one daily talk a day
        self.assertEqual(self.client.post(reverse("talk:go", args=["daily"])).status_code, 402)
        # a finished talk opens its report
        self.assertRedirects(self.client.get(reverse("talk:chat", args=[s.pk])), url)

    def test_roleplay_scripted_and_free_rules(self):
        self.setup_profile()
        self.assertEqual(self.client.post(reverse("talk:go_ref", args=["roleplay", "job-interview"])).status_code, 402)
        self.client.post(reverse("talk:go_ref", args=["roleplay", "cafe-order"]))
        s = TalkSession.objects.get(learner=self.kid, kind="roleplay")
        lines = RP.BY_SLUG["cafe-order"]["lines"]
        self.assertEqual(s.messages[0]["content"], lines[0][0])
        self.assertEqual(self.post_json("talk:api_hint", s.pk).json()["hint"], lines[0][1])
        for i in range(1, 4):
            self.assertEqual(self.post_json("talk:api_reply", s.pk, {"text": "Yes please"}).json()["reply"], lines[i][0])
        self.assertTrue(self.post_json("talk:api_reply", s.pk, {"text": "Thanks"}).json()["done"])
        self.assertEqual(self.client.get(reverse("talk:roleplays") + "?t=popular").status_code, 200)
        self.assertEqual(self.client.post(reverse("talk:go", args=["custom"]), {"setting": "x", "persona": "y"}).status_code, 402)

    def test_read_and_talk(self):
        self.setup_profile()
        r = self.client.get(reverse("talk:read"))
        self.assertContains(r, "Above the clouds in Sajek")
        self.assertNotContains(r, "Slow travel")  # AI topics hidden when AI is off and not written yet
        self.assertContains(self.client.get(reverse("talk:article", args=["travel-sajek"])), "sea of clouds")
        self.assertEqual(self.client.get(reverse("talk:article", args=["science-sleep"])).status_code, 402)
        self.client.post(reverse("talk:go_ref", args=["article", "travel-sajek"]))
        s = TalkSession.objects.get(learner=self.kid, kind="article")
        self.assertIn(T.BY_KEY["travel"]["seed"]["questions"][0], s.messages[0]["content"])
        self.assertIn(T.BY_KEY["travel"]["seed"]["questions"][1], self.post_json("talk:api_reply", s.pk, {"text": "Yes I would"}).json()["reply"])
        self.pay()
        self.assertEqual(self.client.get(reverse("talk:article", args=["travel-t1"])).status_code, 404)  # needs AI

    def test_other_learners_sessions_are_private(self):
        other = Learner.objects.create(family=Family.objects.create(name="O", owner=get_user_model().objects.create_user("o@x.com", "o@x.com", "p-123456789")), name="O")
        s = TE.start(other, "roleplay", "cafe-order")
        self.assertEqual(self.client.get(reverse("talk:chat", args=[s.pk])).status_code, 404)
        self.assertEqual(self.post_json("talk:api_reply", s.pk, {"text": "hi"}).status_code, 404)


@override_settings(AI_API_KEY="test-key")
class TalkAiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("a@example.com", "a@example.com", "safe-pass-123")
        cls.family = Family.objects.create(name="AI family", owner=cls.user, paid_until=date(2099, 1, 1))
        cls.kid = Learner.objects.create(family=cls.family, name="Tania", role="adult")

    def test_reply_tip_report_and_article(self):
        s = TE.start(self.kid, "roleplay", "job-interview")
        with mock.patch("practice.ai.ask", return_value="Nice to meet you. Why this job? (Tip: say 'I worked', not 'I work' for the past)") as m:
            d = TE.reply(self.kid, s, "I work in a bank for five years", .8, 5)
        self.assertEqual(d["reply"], "Nice to meet you. Why this job?")
        self.assertIn("I worked", d["tip"])
        self.assertIn("professional interviewer", m.call_args[0][0])
        report = {"grammar": 72, "best": "I work in a bank for five years", "takeaway": "Use the present perfect for time up to now.",
                  "takeaway_bn": "এখন পর্যন্ত সময়ের জন্য present perfect ব্যবহার করুন।",
                  "better": [{"you": "I work in a bank for five years", "better": "I've worked in a bank for five years.",
                              "tip": "Use the present perfect with 'for'.", "tip_bn": "for-এর সাথে present perfect",
                              "alts": ["I've been working at a bank for five years.", "I've spent five years in banking.", "For five years I've worked in a bank."]}]}
        with mock.patch("practice.ai.ask", return_value="Here you go: " + json.dumps(report)):
            r = TE.finish(self.kid, s)
        self.assertTrue(r["ai"])
        self.assertEqual(r["grammar"], 72)
        self.assertEqual(len(r["better"][0]["alts"]), 3)
        self.assertEqual(r["score"], round((80 + r["fluency"] + 72) / 3))
        self.assertTrue(r["first"])
        self.assertEqual(TE.finish(self.kid, s)["grammar"], 72)  # built once
        art = {"title": "Packing light", "body": "Para one.\n\nPara two.", "questions": ["Q1?", "Q2?", "Q3?"], "words": [["light", "not heavy"]]}
        with mock.patch("practice.ai.ask", return_value=json.dumps(art)):
            a = TE.article("travel-t3")
        self.assertEqual(a["title"], "Packing light")
        self.assertTrue(Article.objects.filter(slug="travel-t3").exists())
        with mock.patch("practice.ai.ask") as m:
            self.assertEqual(TE.article("travel-t3")["questions"][0], "Q1?")
            m.assert_not_called()

    def test_custom_roleplay_and_daily_limit(self):
        with mock.patch("practice.ai.ask", return_value="Good morning, how can I help with your flat?"):
            s = TE.start(self.kid, "custom", setting="Asking my landlord to fix a tap", persona="a busy landlord")
        self.assertEqual(s.messages[0]["content"], "Good morning, how can I help with your flat?")
        with override_settings(), mock.patch.object(TE, "TALK_AI_DAILY", 1), mock.patch("practice.ai.ask") as m:
            d = TE.reply(self.kid, s, "My kitchen tap is leaking")
            m.assert_not_called()
        self.assertTrue(d["done"])  # no AI left and no script → wraps up politely


class TalkApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("p@example.com", "p@example.com", "safe-pass-123")
        cls.family = Family.objects.create(name="Phone family", owner=cls.user)
        cls.kid = Learner.objects.create(family=cls.family, name="Ayaan", role="child")

    def setUp(self):
        self.c = APIClient()
        tok = self.c.post("/api/v1/auth/login/", {"email": "p@example.com", "password": "safe-pass-123"}, format="json").json()["token"]
        self.c.credentials(HTTP_AUTHORIZATION="Token " + tok, HTTP_X_LEARNER=str(self.kid.pk))

    @override_settings(AI_API_KEY="")
    def test_phone_flow(self):
        r = self.c.get("/api/v1/talk/profile/").json()
        self.assertFalse(r["profile"]["done"])
        self.assertEqual(len(r["options"]["interests"]), len(T.CATEGORIES))
        r = self.c.post("/api/v1/talk/profile/", {"level": 2, "reason": "travel", "interests": ["pets", "food", "music"], "speed": 0.6}, format="json").json()
        self.assertTrue(r["profile"]["done"])
        self.assertEqual(r["profile"]["speed"], 0.6)
        home = self.c.get("/api/v1/talk/home/").json()
        self.assertIn(home["daily"]["category"], ["pets", "food", "music"])
        self.assertEqual(home["for_you"][0]["category"], "travel")
        rp = self.c.get("/api/v1/talk/roleplays/").json()
        self.assertEqual(sum(len(c["items"]) for c in rp["categories"]), 41)
        self.assertEqual(self.c.post("/api/v1/talk/start/", {"kind": "roleplay", "ref": "doctor"}, format="json").status_code, 402)
        s = self.c.post("/api/v1/talk/start/", {"kind": "roleplay", "ref": "directions"}, format="json").json()
        self.assertEqual(len(s["messages"]), 1)
        d = self.c.post(f"/api/v1/talk/{s['id']}/reply/", {"text": "Yes, how do I get to the museum?", "confidence": .7}, format="json").json()
        self.assertTrue(d["reply"])
        rep = self.c.post(f"/api/v1/talk/{s['id']}/finish/", format="json").json()["report"]
        self.assertEqual(rep["turns"], 1)
        p = self.c.post(f"/api/v1/talk/{s['id']}/practice/", {"target": "How do I get to the museum?", "said": "how do I get to the museum"}, format="json").json()
        self.assertGreaterEqual(p["score"], 90)
        lib = self.c.get("/api/v1/talk/read/").json()["sections"]
        self.assertEqual(lib[0]["items"][0]["slug"], "travel-sajek")
        self.assertEqual(self.c.get("/api/v1/talk/read/travel-sajek/").json()["title"], "Above the clouds in Sajek")
        self.assertEqual(self.c.get("/api/v1/talk/read/nature-sundarbans/").status_code, 402)
