from datetime import date

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from rest_framework.test import APIClient

from core.models import Family, Learner


class ApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_curriculum", verbosity=0)
        call_command("seed_course", verbosity=0)
        call_command("seed_wordlists", verbosity=0)
        cls.user = get_user_model().objects.create_user("app@example.com", "app@example.com", "safe-pass-123")
        cls.family = Family.objects.create(name="App family", owner=cls.user)
        cls.kid = Learner.objects.create(family=cls.family, name="Nusrat", role="child", birth_year=2016)
        other = get_user_model().objects.create_user("x@example.com", "x@example.com", "safe-pass-123")
        cls.stranger = Learner.objects.create(family=Family.objects.create(name="Other", owner=other), name="Z")

    def setUp(self):
        self.c = APIClient()

    def login(self):
        r = self.c.post("/api/v1/auth/login/", {"email": "APP@example.com", "password": "safe-pass-123"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.c.credentials(HTTP_AUTHORIZATION="Token " + r.json()["token"], HTTP_X_LEARNER=str(self.kid.pk))
        return r.json()

    def test_login(self):
        self.assertEqual(self.c.post("/api/v1/auth/login/", {"email": "app@example.com", "password": "nope"}, format="json").status_code, 400)
        data = self.login()
        self.assertEqual(data["learners"][0]["name"], "Nusrat")
        self.assertFalse(data["family"]["paid"])
        self.assertEqual(self.c.get("/api/v1/me/").status_code, 200)

    def test_needs_token_and_own_learner(self):
        self.assertEqual(self.c.get("/api/v1/today/").status_code, 401)
        self.login()
        self.c.credentials(HTTP_AUTHORIZATION=self.c._credentials["HTTP_AUTHORIZATION"], HTTP_X_LEARNER=str(self.stranger.pk))
        self.assertEqual(self.c.get("/api/v1/today/").status_code, 404)

    def test_today_units_and_free_rules(self):
        self.login()
        r = self.c.get("/api/v1/today/").json()
        self.assertEqual(len(r["tasks"]), 3)
        self.assertIn("journey", r)
        units = self.c.get("/api/v1/units/").json()
        self.assertEqual(len(units), 24)
        self.assertFalse(units[0]["locked"])
        self.assertTrue(units[1]["locked"])
        hello = self.c.get("/api/v1/units/hello/").json()
        self.assertTrue(hello["words"][0]["target"])
        self.assertNotIn("words", self.c.get("/api/v1/units/family/").json())
        # all five lessons can run in the app: grammar data, conversation lines and free speaking
        g = hello["grammar_lesson"]
        self.assertEqual(g["key"], "grammar:a1-be")
        self.assertTrue(g["rule"] and g["examples"] and g["practice"])
        self.assertTrue(hello["conversation"][0]["coach"] and hello["speak_prompt"])
        r = self.c.post("/api/v1/analyse/", {"key": "unit:hello:5", "prompt": hello["speak_prompt"], "seconds": 30,
                                             "transcript": "Hello, my name is Rina and I live in Dhaka with my family. I like reading "
                                                           "books because they are fun, and I also enjoy cooking with my mother."},
                        format="json").json()
        self.assertGreater(r["words"], 20)
        self.assertTrue(0 <= r["overall"] <= 100 and r["tips"][0]["en"])
        self.assertEqual(self.c.post("/api/v1/analyse/", {"key": "unit:family:5", "transcript": "hi", "seconds": 3},
                                     format="json").status_code, 402)
        self.assertEqual(self.c.post("/api/v1/finish/", {"key": "unit:family:1", "score": 90}, format="json").status_code, 402)

    def test_attempt_finish_progress(self):
        self.login()
        r = self.c.post("/api/v1/attempt/", {"key": "unit:hello:1", "target": "thank you", "said": "thank you"}, format="json")
        self.assertGreaterEqual(r.json()["score"], 90)
        r = self.c.post("/api/v1/finish/", {"key": "unit:hello:1", "title": "Hello", "score": 92}, format="json").json()
        self.assertTrue(r["first"])
        self.assertEqual(r["bar"]["gems"], 5)
        p = self.c.get("/api/v1/progress/").json()
        self.assertEqual(p["history"][0]["score"], 92)
        self.assertEqual(len(p["scores"]["parts"]), 5)

    def test_shorts_and_dictionary(self):
        self.login()
        Family.objects.filter(pk=self.family.pk).update(paid_until=date(2099, 1, 1))
        feed = self.c.get("/api/v1/shorts/", {"topic": "food"}).json()
        s = feed["items"][0]
        r = self.c.post("/api/v1/shorts/try/", {"id": s["id"], "said": s["line"]}, format="json").json()
        self.assertGreaterEqual(r["score"], 90)
        self.assertEqual(r["xp"], 5)
        self.assertEqual(self.c.get("/api/v1/dictionary/", {"q": "water"}).json()[0]["word"], "water")
        self.assertEqual(len(self.c.get("/api/v1/grammar/").json()), 41)
