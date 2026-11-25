import datetime as _dt

PAID_UNTIL = _dt.date.today() + _dt.timedelta(days=60)  # tests use a paying family unless they say otherwise
from datetime import date

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from core.models import Family, Learner, PaymentRequest, Plan

from . import planner
from .models import Lesson, Module, PlacementQuestion, PlanDay, Progress
from .placement import score_ladder, score_reader, score_young_child


class SeededTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_curriculum", verbosity=0)
        User = get_user_model()
        cls.user = User.objects.create_user("abba@example.com", "abba@example.com", "safe-pass-123",
                                            first_name="Aziz")
        cls.family = Family.objects.create(name="Bhuiyan family", owner=cls.user, paid_until=PAID_UNTIL)
        cls.child = Learner.objects.create(family=cls.family, name="Rafi", birth_year=2021)


class SeedTests(SeededTestCase):
    def test_phonics_year_is_36_weeks_of_5_days(self):
        for n in (0, 1, 2):
            lessons = Lesson.objects.filter(module__level__number=n)
            self.assertEqual(lessons.count(), 60)
            self.assertEqual(lessons.values("module").distinct().count(), 12)
        first = Lesson.objects.filter(module__level__number=0).first()
        self.assertEqual(first.focus, "/s/")
        self.assertEqual(first.items.count(), 3)
        self.assertEqual(first.module.plan["week"], 1)
        weeks = sorted(m.plan["week"] for m in Module.objects.filter(level__number__lte=2))
        self.assertEqual(weeks, list(range(1, 37)))

    def test_every_lesson_has_video_note_and_task(self):
        for lesson in Lesson.objects.all():
            self.assertTrue(lesson.note_bn, lesson)
            self.assertTrue(lesson.home_task_bn, lesson)
            self.assertGreaterEqual(lesson.videos.count(), 1, lesson)

    def test_quiz_answers_are_among_choices(self):
        for lesson in Lesson.objects.filter(activity__in=["quiz", "sound_tap"]):
            for item in lesson.items.all():
                self.assertIn(item.answer, item.choice_list(), f"{lesson}: {item.prompt}")
        for q in PlacementQuestion.objects.all():
            self.assertIn(q.answer, q.choice_list(), q)

    def test_reseed_is_idempotent(self):
        before = Lesson.objects.count()
        call_command("seed_curriculum", verbosity=0)
        self.assertEqual(Lesson.objects.count(), before)


class PlannerTests(SeededTestCase):
    def test_add_months_clamps_day(self):
        self.assertEqual(planner.add_months(date(2026, 1, 31), 1), date(2026, 2, 28))
        self.assertEqual(planner.add_months(date(2026, 11, 18), 3), date(2027, 2, 18))

    def test_study_dates_follow_sun_to_thu(self):
        days = list(planner.study_dates(date(2026, 11, 15), date(2026, 11, 22), 5))  # Sun 15 .. Sat 21
        self.assertEqual([d.weekday() for d in days], [6, 0, 1, 2, 3])

    def test_too_fast_is_refused(self):
        feas = planner.check(0, 0, 1, 3, date(2026, 11, 15))
        self.assertFalse(feas.ok)
        with self.assertRaises(ValueError):
            planner.build_plan(self.child, 0, 0, 1, 3, start=date(2026, 11, 15))

    def test_build_plan_places_every_lesson_once(self):
        plan = planner.build_plan(self.child, 0, 0, 3, 5, start=date(2026, 11, 15))
        lesson_days = plan.days.filter(kind="lesson")
        self.assertEqual(lesson_days.count(), 60)
        self.assertEqual(plan.days.filter(kind="review").count(), 60 // planner.REVIEW_EVERY)
        self.assertTrue(plan.days.filter(kind="family").exists())
        for d in plan.days.exclude(kind="family"):
            self.assertIn(d.date.weekday(), planner.WEEKDAY_SETS[5])
            self.assertLess(d.date, plan.end_date)
        # lessons stay in teaching order
        keys = [d.lesson.sequence_key() for d in lesson_days.order_by("date", "id")]
        self.assertEqual(keys, sorted(keys))

    def test_new_plan_keeps_finished_lessons_and_deactivates_old(self):
        first = planner.build_plan(self.child, 0, 0, 3, 5, start=date(2026, 11, 15))
        lesson = Lesson.objects.filter(module__level__number=0).first()
        planner.mark_lesson_done(self.child, lesson, score=90)
        second = planner.build_plan(self.child, 0, 1, 6, 5, start=date(2026, 11, 20))
        first.refresh_from_db()
        self.assertFalse(first.is_active)
        self.assertFalse(second.days.filter(lesson=lesson).exists())
        self.assertEqual(Progress.objects.get(learner=self.child, lesson=lesson).stars, 3)

    def test_mission_and_mark_done(self):
        planner.build_plan(self.child, 0, 0, 3, 5, start=date(2026, 11, 15))
        plan, day = planner.today_mission(self.child, date(2026, 11, 15))
        self.assertEqual(day.lesson.focus, "/s/")
        planner.mark_lesson_done(self.child, day.lesson, 40)
        day.refresh_from_db()
        self.assertEqual(day.status, PlanDay.Status.DONE)
        _, nxt = planner.today_mission(self.child, date(2026, 11, 15))
        self.assertNotEqual(nxt.pk, day.pk)


class PlacementTests(SeededTestCase):
    def test_ladder(self):
        self.assertEqual(score_ladder({}, 3, 8), 2)
        self.assertEqual(score_ladder({3: True, 4: True, 5: False, 6: True, 7: False}, 3, 8), 6)
        self.assertEqual(score_ladder({3: True, 4: False, 5: False, 6: True}, 3, 8), 3)

    def test_young_child_all_right_reaches_level_3(self):
        answers = {str(q.id): q.answer for q in PlacementQuestion.objects.filter(skill="phonics")}
        self.assertEqual(score_young_child(answers), 3)
        self.assertEqual(score_young_child({}), 0)

    def test_reader_scores(self):
        answers = {str(q.id): q.answer for q in PlacementQuestion.objects.filter(level__lte=5)
                   .exclude(skill="phonics")}
        levels = score_reader(answers, speaking_level=4)
        self.assertEqual(levels["listening"], 5)
        self.assertEqual(levels["reading"], 5)
        self.assertEqual(levels["speaking"], 4)


class FlowTests(SeededTestCase):
    def setUp(self):
        self.client.force_login(self.user)

    def test_public_pages(self):
        self.client.logout()
        for name in ["core:home", "core:pricing", "core:privacy", "core:signup", "core:login"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_signup_creates_family(self):
        self.client.logout()
        r = self.client.post(reverse("core:signup"), {
            "language": "en", "country": "BD", "phone": "01712-345678",
            "first_name": "Nani", "email": "Nani@Example.com", "family_name": "Nani's family",
            "relation": "Grandmother", "password1": "very-safe-pass-9", "password2": "very-safe-pass-9"})
        self.assertRedirects(r, reverse("world:verify"))
        import re

        from django.core import mail
        code = re.search(r"\b(\d{6})\b", mail.outbox[-1].subject).group(1)
        r = self.client.post(reverse("world:verify"), {"code": code})
        self.assertRedirects(r, reverse("core:learner_add"))
        self.assertTrue(Family.objects.filter(owner__username="nani@example.com").exists())

    def test_full_learning_flow(self):
        self.client.get(reverse("core:choose", args=[self.child.pk]))
        self.assertEqual(self.client.get(reverse("learning:today")).status_code, 200)
        # young-child placement
        answers = {str(q.id): q.answer for q in PlacementQuestion.objects.filter(skill="phonics", level=0)}
        r = self.client.post(reverse("learning:placement_young"), answers)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(self.child.placements.first().overall, 1)
        # plan
        r = self.client.post(reverse("learning:plan_new"), {
            "start_level": 0, "finish_level": 1, "months": 6, "days_per_week": 5,
            "minutes_per_day": 20, "create": "1"})
        self.assertRedirects(r, reverse("learning:plan"))
        self.assertEqual(self.client.get(reverse("learning:plan")).status_code, 200)
        # lesson
        lesson = Lesson.objects.filter(module__level__number=0).first()
        r = self.client.get(reverse("learning:lesson", args=[lesson.pk]))
        self.assertContains(r, "The sound /s/")
        # Long videos and compilations are never embedded; until short clips are found, a link to
        # YouTube videos under 4 minutes is shown instead.
        self.assertNotContains(r, "youtube-nocookie.com/embed/wpoHQN2X8mM")
        self.assertContains(r, "under 4 minutes")
        r = self.client.post(reverse("learning:lesson_complete", args=[lesson.pk]), {"score": "100"})
        self.assertRedirects(r, reverse("learning:today"))
        self.assertEqual(Progress.objects.get(learner=self.child, lesson=lesson).stars, 3)
        self.assertEqual(self.client.get(reverse("learning:library")).status_code, 200)
        self.assertEqual(self.client.get(reverse("core:family")).status_code, 200)

    def test_pin_protects_profile(self):
        self.child.set_pin("1234")
        self.child.save()
        self.client.post(reverse("core:choose", args=[self.child.pk]), {"pin": "0000"})
        self.assertIsNone(self.client.session.get("learner_id"))
        self.client.post(reverse("core:choose", args=[self.child.pk]), {"pin": "1234"})
        self.assertEqual(self.client.session.get("learner_id"), self.child.pk)

    def test_other_family_cannot_open_profile(self):
        other = get_user_model().objects.create_user("x@example.com", "x@example.com", "safe-pass-123")
        Family.objects.create(name="Other", owner=other)
        self.client.force_login(other)
        r = self.client.get(reverse("core:choose", args=[self.child.pk]))
        self.assertEqual(r.status_code, 404)

    def test_co_manager_can_pay_for_family(self):
        nani = get_user_model().objects.create_user("nani@example.com", "nani@example.com", "safe-pass-123")
        self.client.post(reverse("core:manager_add"), {"email": "nani@example.com", "relation": "Grandmother"})
        self.assertTrue(self.family.can_manage(nani))
        self.client.force_login(nani)
        r = self.client.post(reverse("core:pay"), {"plan": Plan.YEAR, "method": "bkash",
                                                   "transaction_id": "TRX123"})
        self.assertRedirects(r, reverse("core:family"))
        pay = PaymentRequest.objects.get(transaction_id="TRX123")
        self.assertEqual(pay.amount_bdt, 2500)
        pay.confirm()
        self.family.refresh_from_db()
        self.assertTrue(self.family.is_paid_active)
        self.assertEqual(self.family.plan, Plan.YEAR)


class TopicVideoTests(SeededTestCase):
    def test_every_lesson_has_a_short_video(self):
        from . import video
        for lesson in Lesson.objects.select_related("module__level").prefetch_related("items"):
            scenes = video.build_scenes(lesson)
            self.assertGreaterEqual(len(scenes), 3, lesson.title)
            self.assertEqual(scenes[0]["kind"], "title")
            self.assertEqual(scenes[-1]["kind"], "outro")
            secs = video.duration_seconds(lesson)
            self.assertTrue(15 <= secs <= 180, f"{lesson.title}: {secs}s")
            for s in scenes:
                self.assertNotIn("/", s.get("say", ""), "phonics slashes must not be read aloud")

    def test_quiz_video_reveals_the_answer(self):
        from . import video
        lesson = Lesson.objects.filter(activity="quiz").exclude(items=None).first()
        scenes = video.build_scenes(lesson)
        answers = [s for s in scenes if s["kind"] == "answer"]
        self.assertEqual(len(answers), lesson.items.count())
        self.assertIn(lesson.items.first().answer, answers[0]["text"])


class DashboardTests(SeededTestCase):
    def setUp(self):
        self.client.force_login(self.user)
        self.client.get(reverse("core:choose", args=[self.child.pk]))

    def test_dashboard_pages(self):
        for name in ["learning:today", "learning:videos", "learning:progress", "learning:library"]:
            r = self.client.get(reverse(name))
            self.assertEqual(r.status_code, 200, name)
            self.assertContains(r, "fe-side")
            self.assertContains(r, "fe-tabbar")

    def test_video_filters(self):
        r = self.client.get(reverse("learning:videos"), {"level": "0"})
        self.assertEqual(r.context["count"], 60)
        r = self.client.get(reverse("learning:videos"), {"skill": "speaking"})
        self.assertTrue(all(c["lesson"].skill == "speaking" for g in r.context["groups"] for c in g["cards"]))
        r = self.client.get(reverse("learning:library"), {"activity": "dictation"})
        self.assertContains(r, "Word dictation")

    def test_lesson_page_has_topic_video(self):
        lesson = Lesson.objects.first()
        r = self.client.get(reverse("learning:lesson", args=[lesson.pk]))
        self.assertContains(r, 'id="tv-scenes"')
        self.assertContains(r, "data-topic-video")

    def test_xp_and_leaderboard(self):
        from . import stats
        parent = Learner.objects.create(family=self.family, name="Ammu", role="adult")
        planner.mark_lesson_done(parent, Lesson.objects.first(), 100)
        board = stats.leaderboard(self.family)
        self.assertEqual(board[0]["learner"], parent)
        self.assertEqual(board[0]["week_xp"], stats.XP_PER_LESSON + 3 * stats.XP_PER_STAR)
