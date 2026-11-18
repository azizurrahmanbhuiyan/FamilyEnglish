import random

from django.core.management.base import BaseCommand
from django.db import transaction

from learning.models import (Lesson, LessonVideo, Level, Module, PlacementQuestion,
                             PracticeItem, Skill)
from learning.seed.levels import LEVELS
from learning.seed.phonics import GROUPS, home_task_bn, note_bn
from learning.seed.placement import PLACEMENT
from learning.seed.upper import UPPER

# A verified compilation from the official Alphablocks channel, used once as an overview.
ALPHABLOCKS_ALPHABET_COMPILATION = "wpoHQN2X8mM"


class Command(BaseCommand):
    help = "Load the FamilyEnglish levels, lessons and placement questions (safe to re-run)."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true",
                            help="Delete existing curriculum and placement questions first")

    @transaction.atomic
    def handle(self, *args, **opts):
        if opts["reset"]:
            Level.objects.all().delete()
            PlacementQuestion.objects.all().delete()

        levels = {}
        for data in LEVELS:
            lv, _ = Level.objects.update_or_create(number=data["number"], defaults=data)
            levels[lv.number] = lv

        self._seed_phonics(levels[0])
        for number, modules in UPPER.items():
            self._seed_upper(levels[number], modules)
        self._seed_placement()

        if opts.get("verbosity", 1) > 0:
            self.stdout.write(self.style.SUCCESS(
            f"Seeded {Level.objects.count()} levels, {Module.objects.count()} modules, "
            f"{Lesson.objects.count()} lessons, {PlacementQuestion.objects.count()} placement questions."))

    def _seed_phonics(self, level):
        all_words = [w for _, _, sounds in GROUPS for s in sounds for w in s[4]]
        rng = random.Random(42)  # stable distractors
        for g_order, (g_name, g_sounds, sounds) in enumerate(GROUPS, 1):
            module, _ = Module.objects.update_or_create(
                level=level, order=g_order,
                defaults=dict(title=f"{g_name}: {g_sounds}",
                              title_bn=f"{g_name} — {g_sounds}",
                              summary_bn="এই দলের ৬টি sound শিখলে অনেক ছোট শব্দ পড়া ও লেখা যাবে।"))
            for s_order, (key, shown, query, action, words, tip) in enumerate(sounds, 1):
                lesson, _ = Lesson.objects.update_or_create(
                    module=module, order=s_order,
                    defaults=dict(
                        title=f"The sound /{shown}/", skill=Skill.PHONICS, minutes=15,
                        focus=f"/{shown}/", action_hint=action,
                        note_bn=note_bn(shown, tip),
                        note_en=f"Say the sound /{shown}/. Do the action: {action}.",
                        home_task_bn=home_task_bn(words),
                        home_task_en="Find 3 things at home with this sound.",
                        activity=Lesson.Activity.SOUND_TAP))
                lesson.videos.all().delete()
                LessonVideo.objects.create(
                    lesson=lesson, order=1, title=f"{query} — letter sound episode",
                    channel="Alphablocks (official)", search_query=f"{query} official phonics",
                    why_watch_bn="এই letter কীভাবে sound দেয় তা ছোট গল্পে দেখায়।", minutes=3)
                if g_order == 1 and s_order == 1:
                    LessonVideo.objects.create(
                        lesson=lesson, order=2,
                        title="Alphabet Learn-A-Thon! | Phonics For Kids Compilation",
                        channel="Alphablocks (official)", youtube_id=ALPHABLOCKS_ALPHABET_COMPILATION,
                        search_query="Alphablocks Alphabet Learn-A-Thon",
                        why_watch_bn="পুরো alphabet-এর sound একসাথে — প্রথম সপ্তাহে কয়েক মিনিট করে দেখুন।",
                        minutes=30)
                lesson.items.all().delete()
                for i, (word, emoji, bn) in enumerate(words, 1):
                    others = [w for w in all_words if w[0] not in {x[0] for x in words}]
                    distractors = rng.sample(others, 2)
                    opts = [f"{emoji} {word}"] + [f"{e} {w}" for w, e, _ in distractors]
                    rng.shuffle(opts)
                    PracticeItem.objects.create(
                        lesson=lesson, order=i, prompt=word, answer=f"{emoji} {word}",
                        choices=", ".join(opts), picture=emoji, meaning_bn=bn)

    def _seed_upper(self, level, modules):
        for m_order, (title, title_bn, lessons) in enumerate(modules, 1):
            module, _ = Module.objects.update_or_create(
                level=level, order=m_order, defaults=dict(title=title, title_bn=title_bn))
            for l_order, (l_title, skill, activity, focus, note, task, videos, items) in enumerate(lessons, 1):
                lesson, _ = Lesson.objects.update_or_create(
                    module=module, order=l_order,
                    defaults=dict(title=l_title, skill=skill, activity=activity, focus=focus,
                                  minutes=20 if level.number >= 3 else 15,
                                  note_bn=note, home_task_bn=task))
                lesson.videos.all().delete()
                for v_order, (v_title, channel, yt, query, why, mins) in enumerate(videos, 1):
                    LessonVideo.objects.create(
                        lesson=lesson, order=v_order, title=v_title, channel=channel,
                        youtube_id=yt, search_query=query, why_watch_bn=why, minutes=mins,
                        made_for_kids=level.number <= 5)
                lesson.items.all().delete()
                for i, item in enumerate(items, 1):
                    if activity == Lesson.Activity.DICTATION:
                        word, emoji, bn = item
                        PracticeItem.objects.create(lesson=lesson, order=i, prompt=word, answer=word,
                                                    picture=emoji, meaning_bn=bn)
                    else:
                        question, answer, choices = item
                        PracticeItem.objects.create(lesson=lesson, order=i, prompt=question,
                                                    answer=answer, choices=choices)

    def _seed_placement(self):
        PlacementQuestion.objects.all().delete()
        for skill, level, prompt, spoken, picture, choices, answer in PLACEMENT:
            PlacementQuestion.objects.create(skill=skill, level=level, prompt=prompt, spoken=spoken,
                                             picture=picture, choices=choices, answer=answer)
