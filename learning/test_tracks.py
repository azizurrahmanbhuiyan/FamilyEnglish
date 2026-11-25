from datetime import date

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from core.models import Family, Learner, PLAN_PRICES_BDT, Plan
from learning import tracks
from learning.models import Lesson, PlanDay, TalkTopic
from learning.planner import add_months


class Base(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_curriculum", verbosity=0)
        call_command("seed_course", verbosity=0)
        call_command("seed_wordlists", verbosity=0)
        cls.user = get_user_model().objects.create_user("f@example.com", "f@example.com", "safe-pass-123")
        cls.family = Family.objects.create(name="Free family", owner=cls.user)   # no plan, no trial
        cls.kid = Learner.objects.create(family=cls.family, name="Rafi", role="child", birth_year=2020)
        cls.nana = Learner.objects.create(family=cls.family, name="Nana", role="adult", birth_year=1955)

    def setUp(self):
        self.client.force_login(self.user)
        s = self.client.session
        s["learner_id"] = self.kid.pk
        s.save()


class PriceAndAccessTests(Base):
    def test_prices(self):
        self.assertEqual(PLAN_PRICES_BDT[Plan.MONTHLY], 299)
        self.assertEqual(PLAN_PRICES_BDT[Plan.HALF_YEAR], 1500)
        self.assertEqual(PLAN_PRICES_BDT[Plan.YEAR], 2500)
        self.assertFalse(self.family.has_full_access)

    def test_phonics_is_free(self):
        for lesson in Lesson.objects.filter(skill="phonics")[:5]:
            self.assertEqual(self.client.get(reverse("learning:lesson", args=[lesson.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("practice:skill_practice", args=["phonics"])).status_code, 200)

    def test_everything_else_is_locked(self):
        other = Lesson.objects.exclude(skill="phonics").first()
        topic = TalkTopic.objects.first()
        for url in [reverse("learning:lesson", args=[other.pk]), reverse("learning:talk_hub"),
                    reverse("learning:talk_topic", args=[topic.slug]), reverse("course:level_test"),
                    reverse("course:lesson", args=["lis-a1"]), reverse("practice:tutor"),
                    reverse("practice:vocab"), reverse("practice:writing"), reverse("practice:reports"),
                    reverse("practice:skill_practice", args=["speaking"])]:
            r = self.client.get(url)
            self.assertEqual(r.status_code, 402, url)
            self.assertContains(r, "৳299", status_code=402)

    def test_paying_opens_everything(self):
        Family.objects.filter(pk=self.family.pk).update(paid_until=date(2099, 1, 1))
        self.assertEqual(self.client.get(reverse("learning:talk_hub")).status_code, 200)
        self.assertEqual(self.client.get(reverse("course:level_test")).status_code, 200)


class TrackTests(Base):
    def test_lengths(self):
        self.assertEqual({k: v["years"] for k, v in tracks.TRACKS.items()},
                         {"kid": 3, "student": 2, "ielts": None, "adult": 1, "elder": 3})
        for key, spec in tracks.TRACKS.items():
            if key != "ielts":
                self.assertEqual(sum(s["months"] for s in spec["stages"]), spec["years"] * 12)
        for m in (3, 6, 9, 12):
            self.assertEqual(tracks.length_months("ielts", m), m)

    def test_ielts_length_follows_the_level_test(self):
        from course.models import SmartTest
        from django.utils import timezone
        self.assertEqual(tracks.recommend_months(self.nana), 12)          # no test yet
        for level, months in ((7, 3), (6, 3), (5, 6), (4, 9), (2, 12)):
            SmartTest.objects.filter(learner=self.nana).delete()
            SmartTest.objects.create(learner=self.nana, finished_at=timezone.now(),
                                     levels={k: level for k in ("listening", "speaking", "reading", "writing")})
            self.assertEqual(tracks.recommend_months(self.nana), months)
            plan = tracks.build_track_plan(self.nana, "ielts", 5, 30, date(2026, 12, 6))
            self.assertEqual(plan.months, months)
            self.assertEqual(plan.end_date, add_months(date(2026, 12, 6), months))
        # the learner can choose another length
        plan = tracks.build_track_plan(self.nana, "ielts", 5, 30, date(2026, 12, 6), months=6)
        self.assertEqual(plan.months, 6)
        self.assertEqual(plan.days.filter(kind="words").count(), 52)       # weeks 53–104 of the 7000

    def test_guessed_track(self):
        self.assertEqual(self.kid.course_track, "kid")
        self.assertEqual(self.nana.course_track, "adult")
        self.nana.track = "elder"
        self.assertEqual(self.nana.course_track, "elder")

    def test_every_track_covers_its_whole_time(self):
        start = date(2026, 12, 6)
        for key, spec in tracks.TRACKS.items():
            plan = tracks.build_track_plan(self.kid, key, 5, 20, start)
            total = tracks.length_months(key, plan.months)
            self.assertEqual(plan.end_date, add_months(start, total))
            days = plan.days.exclude(kind="family")
            last = days.order_by("-date").first().date
            self.assertGreater(last, add_months(start, total - 1))   # runs to the last month
            new = days.exclude(kind="review").count()
            self.assertEqual(new, sum(s["new"] for s in tracks.summary(key, plan.months)))   # every lesson once
            if key != "adult":            # the 1-year parents' course is dense: new items nearly every day
                self.assertTrue(days.filter(kind="review").exists())
            # repeats only come after the item was first taught
            for r in days.filter(kind="review")[:50]:
                first = days.filter(kind__in=["lesson", "course", "topic", "words"], lesson=r.lesson,
                                    course_lesson=r.course_lesson, topic=r.topic, deck=r.deck).first()
                self.assertLess(first.date, r.date)
        self.assertEqual(self.kid.plans.filter(is_active=True).count(), 1)

    def test_kid_year_one_is_sounds_and_daily_talks(self):
        plan = tracks.build_track_plan(self.kid, "kid", 5, 20, date(2026, 12, 6))
        y1 = plan.days.filter(stage__startswith="Year 1").exclude(kind__in=["review", "family"])
        self.assertTrue(all(d.lesson.module.level.number <= 2 for d in y1 if d.lesson_id))
        self.assertEqual(y1.filter(topic__group="daily").count(), TalkTopic.objects.filter(group="daily").count())
        self.assertFalse(y1.filter(course_lesson__isnull=False).exists())

    def test_plan_page_and_finishing_ticks_days(self):
        r = self.client.get(reverse("learning:plan_new"))
        self.assertContains(r, "3 years")
        r = self.client.post(reverse("learning:plan_new"), {"track": "kid", "days_per_week": "5",
                                                            "minutes_per_day": "15"})
        self.assertRedirects(r, reverse("learning:plan"))
        self.kid.refresh_from_db()
        self.assertEqual(self.kid.track, "kid")
        plan = self.kid.plans.get(is_active=True)
        first = plan.days.filter(kind="lesson").first()
        from learning.planner import mark_lesson_done
        mark_lesson_done(self.kid, first.lesson, 100)
        first.refresh_from_db()
        self.assertEqual(first.status, "done")
        # repeats in the future stay to do
        self.assertTrue(plan.days.filter(kind="review", status="todo").exists())
        day = plan.days.filter(kind="review").first()
        self.assertContains(self.client.get(reverse("learning:plan_day", args=[day.pk])), "Repeat")


class WordWeekTests(Base):
    def test_lists(self):
        from practice.models import VocabDeck, VocabWord
        kids = VocabWord.objects.filter(deck__series="kids3000")
        core = VocabWord.objects.filter(deck__series="core7000")
        self.assertEqual(kids.count(), 3000)
        self.assertEqual(core.count(), 7000)
        self.assertEqual(VocabDeck.objects.filter(series="kids3000").count(), 156)
        self.assertEqual(VocabDeck.objects.filter(series="core7000").count(), 104)
        self.assertEqual(kids.values("word").distinct().count(), 3000)
        # British IPA (no final r) and British spelling
        self.assertEqual(kids.get(word="water").ipa, "/ˈwɔːtə/")
        self.assertTrue(kids.filter(word="colour").exists())
        self.assertFalse(core.filter(word="color").exists())
        # the first year of the children's list has Bangla meanings
        self.assertFalse(kids.filter(deck__week__lte=52, meaning_bn="").exists())
        # English definitions for almost every word
        self.assertLess(VocabWord.objects.exclude(deck__series="").filter(definition="").count(), 100)
        self.assertFalse(core.filter(word__in=["peter", "morgan", "managed"]).exists())
        for bad in ("sex", "beer", "kill", "faggot"):
            self.assertFalse(kids.filter(word=bad).exists(), bad)

    def test_week_one_free_others_locked(self):
        r = self.client.get(reverse("practice:word_week", args=["kids3000-w001"]))
        self.assertContains(r, "mother")
        self.assertContains(r, "/ˈmʌðə/")
        self.assertContains(r, "youglish.com/pronounce/mother/english/uk")
        self.assertContains(r, "your female parent; your mum")                 # English meaning first
        self.assertContains(r, '<span class="bn-meaning font-bn" hidden>মা</span>', html=False)  # Bangla on request
        self.assertEqual(self.client.get(reverse("practice:word_week", args=["kids3000-w002"])).status_code, 402)
        self.assertEqual(self.client.get(reverse("practice:words")).status_code, 200)

    def test_write_check_and_finish(self):
        from practice.models import CardReview
        url = reverse("practice:word_write", args=["kids3000-w001"])
        r = self.client.post(url, {"text": "my mother has a baby. My father reads a book"}, follow=True)
        self.assertContains(r, "Start with a capital letter")
        self.assertContains(r, "End with a full stop")
        r = self.client.post(reverse("practice:word_done", args=["kids3000-w001"]), {"score": "9", "total": "12"})
        self.assertEqual(r.status_code, 302)
        self.assertEqual(CardReview.objects.filter(learner=self.kid).count(), 19)

    def test_tracks_include_words_and_pronunciation(self):
        plan = tracks.build_track_plan(self.kid, "kid", 5, 20, date(2026, 12, 6))
        self.assertEqual(plan.days.filter(kind="words").count(), 156)
        plan = tracks.build_track_plan(self.kid, "ielts", 5, 20, date(2026, 12, 6))
        self.assertEqual(plan.days.filter(kind="words").count(), 104)
        self.assertEqual(plan.days.filter(kind="course", course_lesson__slug__startswith="pr-").count(), 41)
        day = plan.days.filter(kind="words").first()
        self.assertContains(self.client.get(reverse("learning:plan_day", args=[day.pk])), "family plan", status_code=200)
