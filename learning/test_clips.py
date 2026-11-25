import datetime as _dt

PAID_UNTIL = _dt.date.today() + _dt.timedelta(days=60)  # tests use a paying family unless they say otherwise
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from core.models import Family, Learner
from course.models import CourseLesson

from . import clips
from .models import Lesson, TalkTopic, VideoClip


def vid(i, title, channel="Alphablocks", duration=180, description="", kids=True):
    return {"id": f"vid{i:08d}", "title": title, "channel": channel, "duration": duration,
            "description": description, "made_for_kids": kids, "embeddable": True}


class ParseTests(TestCase):
    def test_parsers(self):
        self.assertEqual(clips.parse_duration("PT1H2M3S"), 3723)
        self.assertEqual(clips.parse_duration("PT4M"), 240)
        self.assertEqual(clips.parse_time("1:02:03"), 3723)
        self.assertEqual(clips.fmt_time(195), "3:15")
        self.assertEqual(clips.youtube_id("https://www.youtube.com/watch?v=VTNG-HglpU4&list=PL123"), "VTNG-HglpU4")
        self.assertEqual(clips.youtube_id("https://youtu.be/VTNG-HglpU4?t=30"), "VTNG-HglpU4")
        self.assertEqual(clips.youtube_id("https://www.youtube.com/playlist?list=PLBlSS2jp0p"), "")

    def test_chapters(self):
        desc = "Hello!\n0:00 Intro\n1:10 The S sound\n4:30 The A sound\n9:00 Goodbye"
        self.assertEqual(clips.chapters(desc, 600),
                         [(0, 70, "Intro"), (70, 270, "The S sound"), (270, 540, "The A sound"), (540, 600, "Goodbye")])
        self.assertEqual(clips.chapters("1:10 no zero start\n2:00 x", 300), [])


class ChooseTests(TestCase):
    kws = ["s sound", "letter s", "sound s", "/s/"]

    def test_rules(self):
        long_desc = "0:00 Welcome\n2:00 The s sound\n12:00 The t sound"
        cands = [
            vid(1, "Alphabet Learn-A-Thon | Phonics compilation", duration=3600),        # compilation: skip
            vid(2, "The S sound | Phonics for kids", duration=150),                       # short, relevant
            vid(3, "Phonics song: s sound", channel="Random Channel", duration=200),      # untrusted, pending
            vid(4, "Learn phonics with letters", duration=1500, description=long_desc),   # cut to chapter 2:00-7:00
            vid(5, "Cats and dogs", duration=120),                                        # not on topic
            vid(6, "Phonics s sound 2 hours", duration=7200),                             # too long
        ]
        picks = clips.choose(cands, self.kws)
        ids = [p["youtube_id"] for p in picks]
        self.assertNotIn("vid00000001", ids)
        self.assertNotIn("vid00000005", ids)
        self.assertNotIn("vid00000006", ids)
        cut = next(p for p in picks if p["youtube_id"] == "vid00000004")
        self.assertEqual((cut["start"], cut["end"]), (120, 420))  # 5-minute cap inside the chapter
        self.assertFalse(next(p for p in picks if p["youtube_id"] == "vid00000003")["trusted"])
        for p in picks:
            self.assertLessEqual(p["end"] - p["start"], clips.MAX_CLIP)

    def test_twenty_minute_total_and_five_clips(self):
        cands = [vid(i, f"S sound phonics part {i}", duration=290) for i in range(10)]
        picks = clips.choose(cands, self.kws)
        self.assertEqual(len(picks), 4)  # 5 x 290s would be 24 min, so only 4 fit under 20 min
        self.assertLessEqual(sum(p["end"] - p["start"] for p in picks), clips.MAX_TOTAL)
        short = [vid(i, f"S sound phonics {i}", duration=120) for i in range(10)]
        self.assertEqual(len(clips.choose(short, self.kws)), 5)


class FindAndShowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_curriculum", verbosity=0)
        call_command("seed_course", verbosity=0)
        user = get_user_model().objects.create_user("c@example.com", "c@example.com", "safe-pass-123")
        cls.user = user
        cls.family = Family.objects.create(name="Clip family", owner=user, paid_until=PAID_UNTIL)
        cls.kid = Learner.objects.create(family=cls.family, name="Mim", role="child", birth_year=2018)

    def setUp(self):
        self.client.force_login(self.user)
        s = self.client.session
        s["learner_id"] = self.kid.pk
        s.save()

    def test_find_for_saves_trusted_as_shown_and_others_pending(self):
        lesson = Lesson.objects.get(title="The sound /s/")
        fake = [vid(1, "The S sound phonics", duration=100), vid(2, "s sound song", channel="Someone", duration=90),
                vid(3, "Phonics s sound for kids", channel="Jack Hartmann Kids Music Channel", duration=200),
                vid(4, "Letter S sound", channel="Scratch Garden", duration=150),
                vid(5, "Let's learn phonics", duration=100)]
        with mock.patch("learning.clips.search_videos", return_value=fake):
            added = clips.find_for(lesson)
        self.assertEqual(added, 4)  # "Let's learn phonics" is not about /s/, so it is skipped
        self.assertEqual(VideoClip.objects.for_item(lesson).visible().count(), 3)
        self.assertEqual(VideoClip.objects.filter(status="pending").count(), 1)
        with mock.patch("learning.clips.search_videos", return_value=fake) as m:
            self.assertEqual(clips.find_for(lesson), 0)  # already has 4: no more API calls
            m.assert_not_called()
        page = self.client.get(reverse("learning:lesson", args=[lesson.pk]))
        self.assertContains(page, "start=0&amp;end=100")
        self.assertContains(page, "3 clips")
        self.assertNotContains(page, "learn-a-thon")

    def test_fallback_link_is_short_videos_only(self):
        topic = TalkTopic.objects.get(slug="planets")
        page = self.client.get(reverse("learning:talk_topic", args=[topic.slug]))
        self.assertContains(page, "sp=EgIYAQ%253D%253D")
        course = CourseLesson.objects.filter(band="easy").first()
        self.assertContains(self.client.get(reverse("course:lesson", args=[course.slug])), "under 4 minutes")

    def test_clip_limits(self):
        lesson = Lesson.objects.first()
        with self.assertRaises(ValidationError):
            VideoClip(lesson=lesson, youtube_id="VTNG-HglpU4", start=0, end=400).full_clean()
        with self.assertRaises(ValidationError):
            VideoClip(lesson=lesson, youtube_id="https://www.youtube.com/playlist?list=PL1", start=0, end=60).full_clean()
        for i in range(4):
            VideoClip.objects.create(lesson=lesson, youtube_id="VTNG-HglpU4", start=0, end=290)
        with self.assertRaises(ValidationError):  # 4 x 290s + 100s > 20 minutes
            VideoClip(lesson=lesson, youtube_id="VTNG-HglpU4", start=0, end=100).full_clean()

    def test_command_without_key_stops_politely(self):
        from io import StringIO
        out = StringIO()
        call_command("find_clips", "--limit", "2", stdout=out)
        self.assertIn("FE_YOUTUBE_API_KEY", out.getvalue())


class VideoLinkTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from django.core.management import call_command
        call_command("seed_curriculum", verbosity=0)
        call_command("seed_course", verbosity=0)

    def test_every_lesson_has_at_least_five_links(self):
        from course.models import CourseLesson
        from learning.clips import video_links
        from learning.models import Lesson, TalkTopic
        items = list(Lesson.objects.all()) + list(CourseLesson.objects.all()) + list(TalkTopic.objects.all())
        self.assertTrue(items)
        for item in items:
            links = video_links(item)
            yt = [l for l in links if l["kind"] == "youtube"]
            self.assertGreaterEqual(len(yt), 5, item)
            self.assertEqual(len({l["query"] for l in yt}), len(yt), item)  # each link is a different angle
            for l in yt:
                self.assertIn("sp=EgIYAQ", l["url"])  # under 4 minutes
                self.assertNotIn("list=", l["url"])

    def test_phonics_links_are_about_the_sound(self):
        from learning.clips import video_links
        from learning.models import Lesson
        lesson = Lesson.objects.get(title="The sound /s/")
        links = video_links(lesson)
        self.assertTrue(all(" s " in f" {l['query']} " for l in links if l["kind"] == "youtube"))
        self.assertEqual(links[-1]["url"], "https://youglish.com/pronounce/sun/english")
