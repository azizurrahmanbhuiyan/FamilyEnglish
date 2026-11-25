import datetime as _dt

PAID_UNTIL = _dt.date.today() + _dt.timedelta(days=60)  # tests use a paying family unless they say otherwise
import json
from datetime import timedelta
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from core.models import Family, Learner, PaymentRequest, Plan
from learning.models import PlacementQuestion

from . import ai, feedback
from .models import (CardReview, SkillCheck, SpeakingAttempt, SupportTicket, TutorMessage, Tutorial,
                     VocabDeck, VocabWord, WritingAttempt)


class Base(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_curriculum", verbosity=0)
        call_command("seed_practice", verbosity=0)
        User = get_user_model()
        cls.user = User.objects.create_user("abba@example.com", "abba@example.com", "safe-pass-123")
        cls.family = Family.objects.create(name="Bhuiyan family", owner=cls.user, paid_until=PAID_UNTIL)
        cls.child = Learner.objects.create(family=cls.family, name="Rafi", birth_year=2019)

    def setUp(self):
        self.client.force_login(self.user)
        s = self.client.session
        s["learner_id"] = self.child.pk
        s.save()


class SeedTests(Base):
    def test_decks_and_tutorials(self):
        self.assertEqual(VocabDeck.objects.count(), 16)
        self.assertEqual(Tutorial.objects.count(), 10)
        self.assertTrue(all(w.meaning_bn for w in VocabWord.objects.all()))

    def test_reseed_keeps_youtube_id(self):
        t = Tutorial.objects.get(order=1)
        t.youtube_id = "abc123"
        t.save()
        call_command("seed_practice", verbosity=0)
        self.assertEqual(Tutorial.objects.get(order=1).youtube_id, "abc123")
        self.assertEqual(VocabWord.objects.count(), 160)


class PagesTests(Base):
    def test_all_pages_load(self):
        names = ["checks", "dictation", "speaking", "writing", "tutor", "vocab", "vocab_review",
                 "reports", "refer", "tutorials", "support"]
        for n in names:
            r = self.client.get(reverse(f"practice:{n}"))
            self.assertEqual(r.status_code, 200, n)
        for skill in ["phonics", "listening", "reading", "writing"]:
            self.assertEqual(self.client.get(reverse("practice:level_check", args=[skill])).status_code, 200)
            self.assertEqual(self.client.get(reverse("practice:skill_practice", args=[skill])).status_code, 200)
        self.assertEqual(self.client.get(reverse("practice:vocab_deck", args=["animals"])).status_code, 200)
        self.assertEqual(self.client.get(reverse("practice:dictation") + "?level=hard&mode=test").status_code, 200)
        self.assertEqual(self.client.get(reverse("learning:today")).status_code, 200)
        self.assertEqual(self.client.get(reverse("core:family")).status_code, 200)

    def test_tutorials_are_public(self):
        self.client.logout()
        r = self.client.get(reverse("practice:tutorials") + "?n=6")
        self.assertContains(r, "Practise speaking")

    def test_unknown_skill_redirects(self):
        r = self.client.get(reverse("practice:level_check", args=["dancing"]))
        self.assertRedirects(r, reverse("practice:checks"))


class LevelCheckTests(Base):
    def test_reading_check_updates_only_reading(self):
        from learning.placement import save_placement
        save_placement(self.child, {"listening": 4, "speaking": 3, "reading": 3, "writing": 3})
        answers = {str(q.id): q.answer for q in PlacementQuestion.objects.filter(skill="reading", level__lte=6)}
        r = self.client.post(reverse("practice:level_check", args=["reading"]), answers)
        check = SkillCheck.objects.get(learner=self.child, kind="level_check")
        self.assertRedirects(r, reverse("practice:check_result", args=[check.pk]))
        self.assertEqual(check.level, 6)
        p = self.child.placements.first()
        self.assertEqual((p.reading, p.listening, p.speaking), (6, 4, 3))

    def test_phonics_check_sets_all_skills(self):
        answers = {str(q.id): q.answer for q in PlacementQuestion.objects.filter(skill="phonics", level__lte=1)}
        self.client.post(reverse("practice:level_check", args=["phonics"]), answers)
        p = self.child.placements.first()
        self.assertEqual(set(p.skill_levels().values()), {2})

    def test_skill_practice_scores(self):
        r = self.client.get(reverse("practice:skill_practice", args=["speaking"]))
        self.assertRedirects(r, reverse("practice:checks"))
        r = self.client.get(reverse("practice:skill_practice", args=["writing"]))
        items = r.context["items"]
        self.assertTrue(items)
        data = {"item": [str(i.id) for i in items]}
        for n, it in enumerate(items):
            data[f"a{it.id}"] = it.answer if n % 2 == 0 else "wrong"
        r = self.client.post(reverse("practice:skill_practice", args=["writing"]), data)
        check = SkillCheck.objects.get(kind="practice")
        self.assertEqual(check.total, len(items))
        self.assertEqual(check.score, (len(items) + 1) // 2)


class DictationTests(Base):
    def test_word_pools(self):
        from .views import _dictation_words
        for level in ("easy", "medium", "hard"):
            words = _dictation_words(level)
            self.assertGreaterEqual(len(words), 20, level)
            self.assertTrue(all(w["word"].isalpha() for w in words))

    def test_save_is_clamped(self):
        self.client.post(reverse("practice:dictation_save"), {"score": "99", "total": "10",
                                                             "level": "easy", "mode": "practice"})
        c = SkillCheck.objects.get(kind="dictation")
        self.assertEqual((c.score, c.total), (10, 10))


class SpeakingTests(Base):
    def post(self, **data):
        return self.client.post(reverse("practice:speaking_save"), json.dumps(data),
                                content_type="application/json").json()

    def test_repeat_scoring(self):
        d = self.post(target="The frog can jump.", heard="the frog can jump", mode="repeat")
        self.assertEqual(d["score"], 100)
        d = self.post(target="The frog can jump.", heard="the dog can", mode="repeat")
        self.assertIn("frog", d["missed"])
        self.assertEqual(SpeakingAttempt.objects.count(), 2)

    def test_answer_without_ai_gives_tip(self):
        d = self.post(target="Tell me about your family.", heard="I have a mother", mode="answer")
        self.assertEqual(d["score"], 20)
        self.assertIn("because", d["feedback"])
        self.assertFalse(SpeakingAttempt.objects.get().ai_used)


class WritingTests(Base):
    def test_checker_rules(self):
        fixed, notes = feedback.check_writing("my cousin brother go to school. i am agree")
        self.assertEqual(fixed, "My cousin goes to school. I agree.")
        self.assertGreaterEqual(len(notes), 3)
        self.assertEqual(feedback.check_writing("She has an apple.")[1], [])

    def test_writing_page_saves(self):
        r = self.client.post(reverse("practice:writing"), {"text": "she have a egg", "prompt": ""})
        self.assertContains(r, "She has an egg.")
        self.assertFalse(WritingAttempt.objects.get().ai_used)

    @override_settings(AI_API_KEY="test-key")
    def test_writing_uses_ai_when_on(self):
        reply = '{"corrected": "She has an egg.", "notes": ["has ব্যবহার করুন"]}'
        with mock.patch.object(ai, "ask", return_value=reply):
            r = self.client.post(reverse("practice:writing"), {"text": "she have a egg"})
        self.assertContains(r, "has ব্যবহার করুন")
        self.assertTrue(WritingAttempt.objects.get().ai_used)


class TutorTests(Base):
    def test_faq_answer_without_ai(self):
        self.client.post(reverse("practice:tutor"), {"message": "How do I say th?"})
        msgs = list(TutorMessage.objects.filter(learner=self.child))
        self.assertEqual([m.role for m in msgs], ["user", "assistant"])
        self.assertIn("tongue", msgs[1].text)
        self.assertFalse(msgs[1].ai_used)

    @override_settings(AI_API_KEY="test-key", AI_DAILY_LIMIT=1)
    def test_ai_daily_limit(self):
        with mock.patch.object(ai, "ask", return_value="AI answer") as m:
            self.client.post(reverse("practice:tutor"), {"message": "hello"})
            self.client.post(reverse("practice:tutor"), {"message": "how do I say th?"})
        self.assertEqual(m.call_count, 1)
        answers = TutorMessage.objects.filter(role="assistant").order_by("id")
        self.assertEqual(answers[0].text, "AI answer")
        self.assertIn("tongue", answers[1].text)

    def test_faq_matches_common_questions(self):
        self.assertIn("vowel sound", feedback.faq_answer("When do I use an?"))
        self.assertIn("vowel sound", feedback.faq_answer("When do I use “an”?"))
        self.assertIn("past", feedback.faq_answer("What is the past of go?"))

    def test_ai_off_returns_none(self):
        self.assertIsNone(ai.ask("x", [{"role": "user", "content": "hi"}]))

    def test_parent_can_read_but_other_family_cannot(self):
        TutorMessage.objects.create(learner=self.child, role="user", text="What is a noun?")
        r = self.client.get(reverse("practice:tutor_history", args=[self.child.pk]))
        self.assertContains(r, "What is a noun?")
        other = get_user_model().objects.create_user("o@example.com", "o@example.com", "safe-pass-123")
        Family.objects.create(name="Other", owner=other)
        self.client.force_login(other)
        r = self.client.get(reverse("practice:tutor_history", args=[self.child.pk]))
        self.assertEqual(r.status_code, 404)


class VocabTests(Base):
    def test_leitner_boxes(self):
        word = VocabWord.objects.get(word="elephant")
        rate = lambda knew: self.client.post(reverse("practice:vocab_rate"),
                                             json.dumps({"word": word.id, "knew": knew}),
                                             content_type="application/json").json()
        self.assertEqual(rate(True)["box"], 2)
        self.assertEqual(rate(True)["box"], 3)
        review = CardReview.objects.get(learner=self.child, word=word)
        self.assertEqual(review.due, timezone.localdate() + timedelta(days=4))
        self.assertEqual(rate(False)["box"], 1)

    def test_due_cards_come_back(self):
        word = VocabWord.objects.get(word="tiger")
        CardReview.objects.create(learner=self.child, word=word, box=2,
                                  due=timezone.localdate() - timedelta(days=1))
        r = self.client.get(reverse("practice:vocab_review"))
        self.assertEqual([c["word"] for c in r.context["cards"]], ["tiger"])
        r = self.client.get(reverse("practice:vocab"))
        self.assertEqual(r.context["total_due"], 1)

    def test_new_deck_shows_new_cards(self):
        r = self.client.get(reverse("practice:vocab_deck", args=["colours"]))
        self.assertEqual(len(r.context["cards"]), 10)


class ReferralTests(Base):
    def test_full_referral_flow(self):
        code = self.family.referral_code
        self.assertTrue(code and code.startswith("FE"))
        self.client.logout()
        r = self.client.get(reverse("core:signup") + f"?ref={code.lower()}")
        self.assertContains(r, "Invited by Bhuiyan family")
        self.client.post(reverse("core:signup"), {
            "language": "bn", "country": "BD", "phone": "01812345678",
            "first_name": "Nila", "email": "nila@example.com", "family_name": "Nila's family",
            "relation": "Mother", "password1": "very-safe-pass-9", "password2": "very-safe-pass-9"})
        import re

        from django.core import mail
        self.client.post(reverse("world:verify"), {"code": re.search(r"\b(\d{6})\b", mail.outbox[-1].subject).group(1)})
        new = Family.objects.get(owner__username="nila@example.com")
        self.assertEqual(new.referred_by, self.family)
        self.assertEqual((new.trial_ends - new.created_at.date()).days, 7)  # 0 trial + 7 for being invited
        # First payment rewards the inviting family once
        before = self.family.paid_until
        PaymentRequest.objects.create(family=new, plan=Plan.MONTHLY, amount_bdt=299, method="bkash",
                                      transaction_id="T1").confirm()
        self.family.refresh_from_db()
        self.assertEqual(self.family.paid_until, before + timedelta(days=30))
        PaymentRequest.objects.create(family=new, plan=Plan.MONTHLY, amount_bdt=299, method="bkash",
                                      transaction_id="T2").confirm()
        self.family.refresh_from_db()
        self.assertEqual(self.family.paid_until, before + timedelta(days=30))

    def test_refer_page(self):
        r = self.client.get(reverse("practice:refer"))
        self.assertContains(r, self.family.referral_code)
        self.assertContains(r, "wa.me")


class SupportTests(Base):
    def test_ticket(self):
        self.client.post(reverse("practice:support"), {"subject": "bKash", "message": "Paid twice"})
        t = SupportTicket.objects.get()
        self.assertEqual((t.family, t.status), (self.family, "open"))
        r = self.client.get(reverse("practice:support"))
        self.assertContains(r, "Paid twice")
