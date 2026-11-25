import datetime as _dt

PAID_UNTIL = _dt.date.today() + _dt.timedelta(days=60)  # tests use a paying family unless they say otherwise
import json
from datetime import timedelta
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from core.models import Family, Learner, PaymentRequest, Plan, ReferralEarning
from growth import engine
from growth.models import XPEvent
from learning.models import PlanDay
from practice.models import CardReview, SkillCheck, SupportTicket, VocabWord

from . import grading, path, smart_test
from .models import AnswerLog, CourseLesson, CourseProgress, SmartTest


class Base(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_curriculum", verbosity=0)
        call_command("seed_practice", verbosity=0)
        call_command("seed_course", verbosity=0)
        User = get_user_model()
        cls.user = User.objects.create_user("amma@example.com", "amma@example.com", "safe-pass-123")
        cls.family = Family.objects.create(name="Rahman family", owner=cls.user, paid_until=PAID_UNTIL)
        cls.mum = Learner.objects.create(family=cls.family, name="Mina", role="adult", birth_year=1990)

    def setUp(self):
        self.client.force_login(self.user)
        s = self.client.session
        s["learner_id"] = self.mum.pk
        s.save()


class ContentTests(Base):
    def test_every_skill_has_five_lessons_per_category(self):
        for skill in ["listening", "speaking", "reading", "writing", "grammar"]:
            for band in ["easy", "medium", "advanced"]:
                n = CourseLesson.objects.filter(skill=skill, band=band).count()
                self.assertGreaterEqual(n, 5, f"{skill}/{band}")

    def test_every_lesson_has_practice_and_selftest(self):
        for l in CourseLesson.objects.all():
            self.assertGreaterEqual(len(l.practice), 4, l.slug)
            self.assertGreaterEqual(len(l.selftest), 5, l.slug)
            for it in l.practice + l.selftest:
                self.assertTrue(it.get("qt"), l.slug)
                if it["t"] == "choose":
                    self.assertIn(it["a"], it["opts"], l.slug)

    def test_reseed_is_safe(self):
        call_command("seed_course", verbosity=0)
        self.assertEqual(CourseLesson.objects.count(), 118)  # 75 skill lessons + 30 British pronunciation + 13 handbook lessons


class GradingTests(TestCase):
    def test_type_answer_with_word_diff_and_notes(self):
        item = {"t": "type", "a": "He goes to the office every day.", "why": "he → goes"}
        res = grading.check_item(item, "He go to office every day")
        self.assertFalse(res["ok"])
        states = {d["w"]: d["s"] for d in res["diff"]}
        self.assertEqual(states["go"], "wrong")
        self.assertEqual(states["goes"], "missing")
        self.assertTrue(res["notes"])  # built-in checker explains in Bangla
        self.assertTrue(grading.check_item(item, "he goes to the office every day")["ok"])

    def test_exact_items_check_capitals_and_full_stops(self):
        item = {"t": "type", "a": "I live in Dhaka.", "exact": True}
        self.assertFalse(grading.check_item(item, "i live in dhaka")["ok"])
        self.assertTrue(grading.check_item(item, "I live in Dhaka.")["ok"])

    def test_accept_list(self):
        item = {"t": "type", "a": "7:30", "accept": ["07:30"]}
        self.assertTrue(grading.check_item(item, "07:30")["ok"])

    def test_say_and_open(self):
        say = {"t": "say", "a": "This is my mother."}
        res = grading.check_item(say, "this is my brother")
        self.assertFalse(res["ok"])
        self.assertIn("mother", res["missed"])
        open_item = {"t": "open", "q": "Write about you", "min": 10}
        short = grading.check_item(open_item, "i like rice")
        self.assertFalse(short["ok"])
        good = grading.check_item(open_item, "I am ten years old. I like rice and fish. I live in Dhaka with my family.")
        self.assertTrue(good["ok"])

    def test_public_item_hides_answers(self):
        pub = grading.public_item({"t": "choose", "q": "Q", "a": "x", "opts": ["x", "y"], "why": "w"})
        self.assertNotIn("a", pub)
        self.assertNotIn("why", pub)


class LessonFlowTests(Base):
    def test_lesson_page_has_no_answers(self):
        l = CourseLesson.objects.get(slug="gr-e1")
        r = self.client.get(reverse("course:lesson", args=[l.slug]))
        self.assertEqual(r.status_code, 200)
        self.assertNotContains(r, "My father is an engineer.")  # a 'type' answer stays on the server

    def test_practice_check_logs_answer_and_explains(self):
        l = CourseLesson.objects.get(slug="gr-e1")
        idx = next(i for i, it in enumerate(l.practice) if it["t"] == "type")
        r = self.client.post(reverse("course:check"), json.dumps({"slug": l.slug, "i": idx, "answer": "My father is engineer."}),
                             content_type="application/json")
        data = r.json()
        self.assertFalse(data["ok"])
        self.assertTrue(any(d["s"] == "missing" and d["w"] == "an" for d in data["diff"]))
        self.assertTrue(AnswerLog.objects.filter(learner=self.mum, correct=False, qtype="gr_articles").exists())

    def test_bad_check_request(self):
        r = self.client.post(reverse("course:check"), json.dumps({"slug": "nope", "i": 0}), content_type="application/json")
        self.assertEqual(r.status_code, 400)

    def _answers(self, lesson, right=True):
        data = {}
        for i, it in enumerate(lesson.selftest):
            if right:
                data[f"a{i}"] = it["a"]
            else:
                data[f"a{i}"] = "zzz"
        return data

    def test_selftest_pass_gives_progress_xp_and_marks_plan_day(self):
        l = CourseLesson.objects.get(slug="gr-e2")
        self.client.post(reverse("course:practice_done", args=[l.slug]))
        plan = path.build_path(self.mum)
        from learning import planner
        planner.build_course_plan(self.mum, [l] + plan[:5], 1, 5, 20, timezone.localdate())
        r = self.client.post(reverse("course:selftest", args=[l.slug]), self._answers(l))
        self.assertEqual(r.status_code, 302)
        prog = CourseProgress.objects.get(learner=self.mum, lesson=l)
        self.assertTrue(prog.passed)
        self.assertEqual(prog.stars, 3)
        self.assertEqual(engine.totals(self.mum)["xp"], 10 + 30 + 30)
        self.assertTrue(PlanDay.objects.get(course_lesson=l).status == "done")
        result = self.client.get(r["Location"])
        self.assertContains(result, "100%")

    def test_selftest_fail_shows_fixes(self):
        l = CourseLesson.objects.get(slug="wr-e1")
        r = self.client.post(reverse("course:selftest", args=[l.slug]), self._answers(l, right=False), follow=True)
        self.assertContains(r, "Right answer")
        self.assertFalse(CourseProgress.objects.get(learner=self.mum, lesson=l).passed)
        self.assertEqual(engine.totals(self.mum)["xp"], 0)

    def test_free_family_gets_the_locked_page_for_the_course(self):
        Family.objects.filter(pk=self.family.pk).update(created_at=timezone.now() - timedelta(days=60),
                                                         paid_until=None)
        for band in ("easy", "medium", "advanced"):
            l = CourseLesson.objects.filter(band=band).first()
            r = self.client.get(reverse("course:lesson", args=[l.slug]))
            self.assertEqual(r.status_code, 402)
            self.assertContains(r, "299", status_code=402)
        self.assertEqual(self.client.get(reverse("course:level_test")).status_code, 402)
        self.assertEqual(self.client.get(reverse("course:home")).status_code, 200)

    def test_pages(self):
        for name, args in [("home", []), ("weak_spots", []), ("level_test", []), ("drill", ["gr_tense"]),
                           ("skill", ["listening"]), ("lesson", ["lis-a1"]), ("selftest", ["spk-m2"])]:
            self.assertEqual(self.client.get(reverse(f"course:{name}", args=args)).status_code, 200, name)


class SmartTestTests(Base):
    def _run(self, objective_right=True, writing="", speaking_open=""):
        self.client.post(reverse("course:level_start"))
        test = SmartTest.objects.filter(learner=self.mum).first()
        for _ in range(12):
            test.refresh_from_db()
            step = smart_test.current_step(test)
            if step is None:
                break
            skill = step.split(":")[0]
            if skill in smart_test.OBJECTIVE:
                data = {f"q{i}": (it["a"] if objective_right else "nope")
                        for i, it in enumerate(smart_test.items_for(step))}
            elif skill == "writing":
                data = {"text": writing}
            else:
                sp = smart_test.speaking_tasks(self.mum)
                data = {"r0": sp["repeat"][0], "r1": sp["repeat"][1], "open": speaking_open}
            self.client.post(reverse("course:level_step", args=[test.pk]), data)
        self.client.get(reverse("course:level_step", args=[test.pk]))
        test.refresh_from_db()
        return test

    def test_strong_learner_gets_advanced_rounds_and_high_levels(self):
        essay = ("I strongly believe that parents should learn English with their children. Firstly, it helps "
                 "children feel confident because they can practise at home every day. Moreover, parents "
                 "improve their own English, which is useful at work. For example, my neighbour and her son "
                 "watch short videos together and then talk about them in English. However, families need "
                 "simple materials and a little time. Therefore, learning together is a practical idea.")
        talk = ("my aunt helped me learn to ride a bicycle when I was eight because my parents were busy "
                "first she held the seat and ran beside me then she let go without telling me and I realised "
                "I was riding alone after that I practised every evening and finally I could ride to school "
                "so I learned that being patient and brave is important and I still thank her for that")
        test = self._run(True, essay, talk)
        self.assertTrue(test.done)
        self.assertIn("listening:2", test.steps)  # adaptive: advanced round added
        self.assertGreaterEqual(test.levels["listening"], 7)
        self.assertEqual(test.bands["grammar"], "advanced")
        self.assertGreaterEqual(test.levels["writing"], 5)
        self.assertTrue(test.report.get("summary_bn"))
        self.assertEqual(self.mum.placements.first().listening, test.levels["listening"])
        self.assertEqual(engine.totals(self.mum)["xp"], 50)
        r = self.client.get(reverse("course:level_result", args=[test.pk]))
        self.assertContains(r, "Your lessons, in order")

    def test_beginner_gets_easy_and_path_starts_with_weakest(self):
        test = self._run(False, "i like rice", "yes")
        self.assertNotIn("listening:2", test.steps)
        self.assertEqual(test.bands["listening"], "easy")
        lessons = path.build_path(self.mum)
        self.assertEqual(lessons[0].band, "easy")
        weakest = test.weakest()
        self.assertEqual(lessons[0].skill, weakest)
        first_ten = [l.skill for l in lessons[:10]]
        self.assertGreater(first_ten.count(weakest), first_ten.count("reading" if weakest != "reading" else "grammar"))

    @override_settings(AI_API_KEY="test-key")
    def test_ai_marks_writing_when_on(self):
        reply = json.dumps({"level": 6, "strengths": ["clear"], "fixes": [], "comment_bn": "ভালো"})
        with mock.patch("practice.ai.ask", return_value=reply):
            test = self._run(True, "Some writing here that is long enough to be marked by the examiner.", "hello")
        self.assertEqual(test.levels["writing"], 6)
        self.assertTrue(test.ai_used)

    def test_course_plan_from_path(self):
        self._run(False, "i like rice", "yes")
        r = self.client.post(reverse("course:path_plan"), {"months": 3, "days_per_week": 5, "minutes": 20})
        self.assertEqual(r.status_code, 302)
        plan = self.mum.plans.get(is_active=True)
        self.assertEqual(plan.kind, "course")
        self.assertTrue(plan.days.filter(kind="course").exists())
        self.assertEqual(self.client.get(reverse("learning:today")).status_code, 200)
        self.assertEqual(self.client.get(reverse("learning:plan")).status_code, 200)
        day = plan.days.filter(kind="course").first()
        self.assertContains(self.client.get(reverse("learning:plan_day", args=[day.pk])), "Why this task today?")
        self.client.post(reverse("learning:plan_restart"))
        self.assertEqual(self.mum.plans.get(is_active=True).start_date, timezone.localdate())


class GrowthTests(Base):
    def test_streak_freezes_cover_one_missed_day(self):
        today = timezone.localdate()
        for back in (0, 2, 3):  # yesterday missed
            XPEvent.objects.create(learner=self.mum, amount=5, reason="x",
                                   created_at=timezone.now() - timedelta(days=back))
        info = engine.streak_info(self.mum, today)
        self.assertEqual(info["streak"], 3)
        self.assertEqual(len(info["frozen_days"]), 1)

    def test_long_gap_breaks_streak_without_using_freezes(self):
        for back in (0, 10):
            XPEvent.objects.create(learner=self.mum, amount=5, reason="x",
                                   created_at=timezone.now() - timedelta(days=back))
        info = engine.streak_info(self.mum)
        self.assertEqual(info["streak"], 1)
        self.assertEqual(info["freezes_left"], 3)

    def test_award_is_once_per_key(self):
        self.assertTrue(engine.award(self.mum, 10, "t", key="k1"))
        self.assertFalse(engine.award(self.mum, 10, "t", key="k1"))
        self.assertEqual(engine.totals(self.mum)["xp"], 10)

    def test_league_promotion_and_privacy(self):
        other_user = get_user_model().objects.create_user("x@example.com", "x@example.com", "safe-pass-123")
        other = Family.objects.create(name="Other", owner=other_user)
        kid = Learner.objects.create(family=other, name="Secretname", avatar="🐯")
        last_week = engine.week_start() - timedelta(days=3)
        XPEvent.objects.create(learner=self.mum, amount=100, reason="x",
                               created_at=timezone.make_aware(timezone.datetime.combine(last_week, timezone.datetime.min.time())) + timedelta(hours=12))
        engine.settle_leagues()
        self.mum.refresh_from_db()
        self.assertEqual(self.mum.league, "silver")
        Learner.objects.filter(pk=kid.pk).update(league="silver")
        r = self.client.get(reverse("growth:leaderboard"))
        self.assertNotContains(r, "Secretname")
        self.assertContains(r, "Tiger")

    def test_pages_and_goals(self):
        for name in ["streaks", "leaderboard", "profile", "ideas", "whats_new"]:
            self.assertEqual(self.client.get(reverse(f"growth:{name}")).status_code, 200, name)
        self.client.post(reverse("growth:goals"), {"xp": 50, "questions": 20, "lessons": 2})
        self.assertEqual(engine.goal_for(self.mum).xp, 50)

    def test_badges(self):
        b = engine.badges(self.mum)
        self.assertEqual(len(b), 15)
        self.assertFalse(any(x["earned"] for x in b))

    def test_language_switch(self):
        self.client.get(reverse("growth:lang", args=["bn"]), HTTP_REFERER="/learn/")
        r = self.client.get(reverse("course:home"))
        self.assertContains(r, "আমার কোর্স")

    def test_ideas_and_votes(self):
        self.client.post(reverse("growth:ideas"), {"title": "Bedtime stories", "details": "please"})
        from growth.models import FeatureIdea, FeatureVote
        idea = FeatureIdea.objects.get()
        self.assertEqual(FeatureVote.objects.filter(idea=idea).count(), 1)
        self.client.post(reverse("growth:vote", args=[idea.pk]))
        self.assertEqual(FeatureVote.objects.filter(idea=idea).count(), 0)

    def test_dashboard_with_xp_panel(self):
        engine.award(self.mum, 25, "test")
        r = self.client.get(reverse("learning:today"))
        self.assertContains(r, 'title="XP"><svg')
        self.assertContains(r, "</svg><b>25</b></a>")
        self.assertContains(self.client.get(reverse("studio:more")), "AI level test")
        self.assertNotContains(r, "dash-new\">AI")


class PracticeUpgradeTests(Base):
    def test_flashcard_three_grades(self):
        word = VocabWord.objects.first()
        url = reverse("practice:vocab_rate")
        post = lambda g: self.client.post(url, json.dumps({"word": word.id, "grade": g}), content_type="application/json").json()
        self.assertEqual(post(2)["box"], 2)
        self.assertEqual(post(1)["box"], 2)  # almost: same box
        self.assertEqual(post(0)["box"], 1)
        self.assertEqual(CardReview.objects.get(word=word).last_grade, 0)
        self.assertEqual(self.client.get(reverse("practice:vocab_review") + "?mode=missed").status_code, 200)
        self.assertContains(self.client.get(reverse("practice:vocab_deck", args=[word.deck.slug]) + "?view=list"), word.word)
        self.assertGreater(engine.totals(self.mum)["xp"], 0)

    def test_typing_and_dictation_mixed(self):
        self.assertEqual(self.client.get(reverse("practice:typing")).status_code, 200)
        self.client.post(reverse("practice:typing_save"), {"wpm": 35, "accuracy": 96, "seconds": 60, "level": "easy"})
        self.assertEqual(SkillCheck.objects.get(kind="typing").score, 35)
        r = self.client.get(reverse("practice:dictation") + "?level=mixed&mode=test")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "MAX_PLAYS")

    def test_support_screenshot_checks(self):
        png = SimpleUploadedFile("s.png", b"\x89PNG\r\n\x1a\n" + b"0" * 50, content_type="image/png")
        self.client.post(reverse("practice:support"), {"subject": "Help", "message": "Hi", "attachment": png})
        t = SupportTicket.objects.get()
        self.assertTrue(t.attachment)
        self.assertEqual(self.client.get(reverse("practice:support_file", args=[t.pk])).status_code, 200)
        t.attachment.delete()
        fake = SimpleUploadedFile("s.png", b"not an image", content_type="image/png")
        self.client.post(reverse("practice:support"), {"subject": "Help 2", "message": "Hi", "attachment": fake})
        self.assertEqual(SupportTicket.objects.count(), 1)

    def test_referral_commission_and_payout(self):
        friend_user = get_user_model().objects.create_user("f@example.com", "f@example.com", "safe-pass-123")
        friend = Family.objects.create(name="Friend", owner=friend_user, referred_by=self.family)
        pay = PaymentRequest.objects.create(family=friend, plan=Plan.YEAR, amount_bdt=5000, method="bkash",
                                            transaction_id="TX1")
        pay.confirm()
        e = ReferralEarning.objects.get()
        self.assertEqual(e.amount_bdt, 500)
        ReferralEarning.objects.update(available_on=timezone.localdate())
        self.client.post(reverse("practice:refer"), {"bkash": "01711000000"})
        self.assertEqual(self.family.payouts.get().amount_bdt, 500)

    def test_writing_model_answer_without_ai(self):
        r = self.client.post(reverse("practice:writing"), {"action": "model", "prompt": "My best friend"})
        self.assertContains(r, "Model answer")

    def test_writing_level_estimate(self):
        r = self.client.post(reverse("practice:writing"), {"text": "I like my school. My teacher is kind. We play football."})
        self.assertContains(r, "Estimated writing level")

    def test_tutor_greeting(self):
        self.assertContains(self.client.get(reverse("practice:tutor")), "Hi Mina")

    def test_devices_listed_and_sign_out_others(self):
        self.client.get(reverse("learning:today"))
        self.assertContains(self.client.get(reverse("growth:profile")), "this device")
        r = self.client.post(reverse("growth:signout_others"))
        self.assertEqual(r.status_code, 302)


class HandbookTests(Base):
    def test_every_handout_file_and_lesson_exists(self):
        from . import handouts
        slugs = set(CourseLesson.objects.values_list("slug", flat=True))
        self.assertEqual(len(handouts.HANDOUTS), 23)
        for n, (_, _, lessons) in handouts.HANDOUTS.items():
            self.assertTrue(handouts.path(n).exists(), n)
            for s in lessons:
                self.assertIn(s, slugs, (n, s))

    def test_paid_family_downloads_and_lesson_links(self):
        r = self.client.get(reverse("course:handout", args=[13]))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r["Content-Type"], "application/pdf")
        self.assertTrue(b"".join(r.streaming_content).startswith(b"%PDF"))
        self.assertContains(self.client.get(reverse("course:lesson", args=["pr-h13"])), "Handbook PDF")
        self.assertContains(self.client.get(reverse("course:handbook")), "Silent letters")
        self.assertEqual(self.client.get(reverse("course:handout", args=[99])).status_code, 404)

    def test_free_family_gets_only_01_and_02(self):
        Family.objects.filter(pk=self.family.pk).update(paid_until=None)
        self.assertEqual(self.client.get(reverse("course:handout", args=[1])).status_code, 200)
        self.assertEqual(self.client.get(reverse("course:handout", args=[2])).status_code, 200)
        self.assertEqual(self.client.get(reverse("course:handout", args=[3])).status_code, 402)
        self.assertContains(self.client.get(reverse("course:handbook")), "Family plan")

    def test_handbook_lessons_reach_student_and_ielts_plans(self):
        from learning import tracks
        from datetime import date
        stu = Learner.objects.create(family=self.family, name="Rafi", role="kid", birth_year=2012)
        plan = tracks.build_track_plan(stu, "student", 5, 30, date(2026, 12, 6))
        got = set(plan.days.filter(kind="course").values_list("course_lesson__slug", flat=True))
        self.assertTrue({"pr-h01", "pr-h08", "pr-h18", "pr-h21"} <= got, got)
        plan = tracks.build_track_plan(self.mum, "ielts", 5, 20, date(2026, 12, 6))
        got = set(plan.days.filter(kind="course").values_list("course_lesson__slug", flat=True))
        self.assertTrue({"pr-h19", "pr-h20", "pr-h21"} <= got, got)
