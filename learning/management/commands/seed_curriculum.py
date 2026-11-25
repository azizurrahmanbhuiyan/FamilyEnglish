import random

from django.core.management.base import BaseCommand
from django.db import transaction

from learning.models import (Lesson, LessonVideo, Level, Module, PlacementQuestion,
                             PracticeItem, Skill)
from learning.seed.levels import LEVELS
from learning import phonics_year
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

        self._seed_phonics_year(levels)
        for number, modules in UPPER.items():
            if number >= 3:  # levels 0-2 are the Phonics Year
                self._seed_upper(levels[number], modules)
        self._seed_placement()
        from django.core.management import call_command
        call_command("seed_family_talk", verbosity=0)
        call_command("seed_talk_topics", verbosity=0)

        if opts.get("verbosity", 1) > 0:
            self.stdout.write(self.style.SUCCESS(
            f"Seeded {Level.objects.count()} levels, {Module.objects.count()} modules, "
            f"{Lesson.objects.count()} lessons, {PlacementQuestion.objects.count()} placement questions."))

    def _seed_phonics_year(self, levels):
        """36 weeks x 5 days: weeks 1-12 -> Level 0, 13-24 -> Level 1, 25-36 -> Level 2. One module per week."""
        kept = {0: set(), 1: set(), 2: set()}
        for wk, prepare, days in phonics_year.build():
            level = levels[wk["term"] - 1]
            order = (wk["n"] - 1) % 12 + 1
            module, _ = Module.objects.update_or_create(
                level=level, order=order,
                defaults=dict(title=f"Week {wk['n']}: {wk['title']}", title_bn=f"সপ্তাহ {wk['n']}: {wk['title_bn']}",
                              summary_bn="", plan={"week": wk["n"], "term": wk["term"], "goal": wk["goal"],
                                                   "prepare": prepare, "tricky": wk["tricky"]}))
            kept[level.number].add(module.pk)
            keep_lessons = []
            for d_order, d in enumerate(days, 1):
                lesson, _ = Lesson.objects.update_or_create(
                    module=module, order=d_order,
                    defaults=dict(title=d["title"], skill=Skill.PHONICS, minutes=d["minutes"], focus=d["focus"],
                                  action_hint=d["action_hint"], note_bn=d["note_bn"], note_en=d["note_en"],
                                  home_task_bn=d["home_task_bn"], home_task_en=d["home_task_en"],
                                  activity=d["activity"], teacher=d["teacher"]))
                keep_lessons.append(lesson.pk)
                lesson.videos.all().delete()
                if d["kind"] == "sound":
                    LessonVideo.objects.create(
                        lesson=lesson, order=1, title=f"{d['focus']} — letter sound episode", channel="Alphablocks (official)",
                        search_query=f"Alphablocks {d['focus'].replace('/', '').split(' and ')[0]} official phonics",
                        why_watch_bn="এই sound কীভাবে বলে তা ছোট গল্পে দেখায়।", minutes=3)
                else:
                    LessonVideo.objects.create(
                        lesson=lesson, order=1, title=f"{d['title']} — related episode", channel="Alphablocks (official)",
                        search_query=f"Alphablocks {d['focus'].split(' · ')[0]} phonics",
                        why_watch_bn="এই সপ্তাহের বিষয় নিয়ে ছোট ভিডিও খুঁজে একসাথে দেখুন।", minutes=5)
                if d["kind"] == "sound" and wk["n"] == 1 and d_order == 1:
                        LessonVideo.objects.create(
                            lesson=lesson, order=2, title="Alphabet Learn-A-Thon! | Phonics For Kids Compilation",
                            channel="Alphablocks (official)", youtube_id=ALPHABLOCKS_ALPHABET_COMPILATION,
                            search_query="Alphablocks Alphabet Learn-A-Thon",
                            why_watch_bn="পুরো alphabet-এর sound একসাথে — প্রথম সপ্তাহে কয়েক মিনিট করে দেখুন।", minutes=30)
                lesson.items.all().delete()
                PracticeItem.objects.bulk_create([
                    PracticeItem(lesson=lesson, order=i, prompt=p[:200], answer=a[:120], choices=c[:300], picture=e, meaning_bn=bn[:120])
                    for i, (p, a, c, e, bn) in enumerate(d["items"], 1)])
            module.lessons.exclude(pk__in=keep_lessons).delete()
        for number, pks in kept.items():
            Module.objects.filter(level=levels[number]).exclude(pk__in=pks).delete()

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
