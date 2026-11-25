"""Full courses with a fixed length, by kind of learner.

    Young child (3–10)                      3 years   the 36-week Phonics Year, then 3000 words and British sounds
    School student (class 6–10)             2 years   7000 words, skill course, British pronunciation
    IELTS / university                      3–12 months, by level test result (7000-word range, Advanced skills)
    Parent who studied at school/college    1 year    3000 words, everything to Advanced
    Grandparent or adult who studied little 3 years   3000 words, slow and steady

Each stage mixes: level lessons, talk-at-home topics, skill-course lessons, British pronunciation
lessons and weekly word sets (listen, say, spell, write).

Each course is split into stages. Inside a stage the new lessons are spread evenly over the study
days; the days in between repeat earlier lessons (spaced practice), because children and adults who
studied little need many repeats to speak without fear. Fridays are family days.
"""

from datetime import timedelta

from django.db import transaction

from .models import Lesson, PlanDay, StudyPlan, TalkTopic
from .planner import FRIDAY, MAX_PER_DAY, add_months, study_dates

TRACKS = {
    "kid": {
        "years": 3, "en": "Young child (3–10 years)", "bn": "ছোট শিশু (৩–১০ বছর)",
        "why_en": "Young children learn by hearing, saying and repeating a little every day.",
        "why_bn": "ছোট শিশুরা প্রতিদিন একটু একটু শুনে, বলে আর বারবার করে শেখে।",
        "stages": [
            {"months": 12, "en": "Year 1 · The Phonics Year (36 weeks)", "bn": "১ম বছর · ফনিক্স বছর (৩৬ সপ্তাহ)",
             "levels": [0, 1, 2], "topics": ["daily"], "bands": [], "pron": [], "words": None},
            {"months": 12, "en": "Year 2 · Reading and everyday talk", "bn": "২য় বছর · পড়া ও প্রতিদিনের কথা",
             "levels": [3, 4], "topics": ["study"], "bands": [], "pron": ["easy"], "words": ("kids3000", 1, 78)},
            {"months": 12, "en": "Year 3 · A confident little speaker", "bn": "৩য় বছর · আত্মবিশ্বাসী ছোট বক্তা",
             "levels": [5, 6, 7, 8], "topics": ["trip"], "bands": ["easy"], "pron": ["medium"], "words": ("kids3000", 79, 156)},
        ],
    },
    "student": {
        "years": 2, "en": "School student (class 6–10)", "bn": "স্কুলের শিক্ষার্থী (৬ষ্ঠ–১০ম শ্রেণি)",
        "why_en": "Students already read; two years fix the sounds, grammar and the fear of speaking.",
        "why_bn": "শিক্ষার্থীরা পড়তে পারে; দুই বছরে উচ্চারণ, ব্যাকরণ আর কথা বলার ভয় ঠিক হয়।",
        "stages": [
            {"months": 12, "en": "Year 1 · Strong basics", "bn": "১ম বছর · মজবুত ভিত",
             "levels": [2, 3, 4], "topics": ["daily", "study"], "bands": ["easy"], "pron": ["easy", "medium"], "words": ("core7000", 1, 52)},
            {"months": 12, "en": "Year 2 · Fluent and exam-ready", "bn": "২য় বছর · সাবলীল ও পরীক্ষার জন্য প্রস্তুত",
             "levels": [5, 6, 7, 8], "topics": ["trip"], "bands": ["medium", "advanced"], "pron": ["advanced"], "words": ("core7000", 53, 104)},
        ],
    },
    "ielts": {
        "years": None, "months_options": [3, 6, 9, 12],
        "en": "IELTS or university preparation", "bn": "IELTS বা বিশ্ববিদ্যালয়ের প্রস্তুতি",
        "why_en": "3 to 12 months, depending on your level test: words up to 7000, Advanced skills and clear "
                  "British pronunciation for band 6.5–7+. Plan 30–45 minutes a day.",
        "why_bn": "লেভেল টেস্ট অনুযায়ী ৩ থেকে ১২ মাস: ৭০০০ পর্যন্ত শব্দ, অ্যাডভান্সড দক্ষতা ও স্পষ্ট ব্রিটিশ উচ্চারণ — "
                  "ব্যান্ড ৬.৫–৭+ এর জন্য। দিনে ৩০–৪৫ মিনিট রাখুন।",
        "variants": {
            3: [
                {"months": 2, "en": "Months 1–2 · Advanced skills and pronunciation", "bn": "১–২ মাস · অ্যাডভান্সড দক্ষতা ও উচ্চারণ",
                 "levels": [], "topics": [], "bands": ["advanced"], "pron": ["advanced"], "words": ("core7000", 79, 95)},
                {"months": 1, "en": "Month 3 · Exam fluency", "bn": "৩য় মাস · পরীক্ষার জন্য সাবলীলতা",
                 "levels": [7, 8], "topics": [], "bands": [], "pron": [], "words": ("core7000", 96, 104)},
            ],
            6: [
                {"months": 3, "en": "Months 1–3 · Upper-intermediate", "bn": "১–৩ মাস · আপার-ইন্টারমিডিয়েট",
                 "levels": [5, 6], "topics": [], "bands": ["medium"], "pron": ["medium"], "words": ("core7000", 53, 78)},
                {"months": 3, "en": "Months 4–6 · Band 6.5 and above", "bn": "৪–৬ মাস · ব্যান্ড ৬.৫ ও তার বেশি",
                 "levels": [7, 8], "topics": [], "bands": ["advanced"], "pron": ["advanced"], "words": ("core7000", 79, 104)},
            ],
            9: [
                {"months": 3, "en": "Months 1–3 · Accurate basics", "bn": "১–৩ মাস · নির্ভুল ভিত্তি",
                 "levels": [3, 4], "topics": [], "bands": ["easy"], "pron": ["easy"], "words": ("core7000", 27, 52)},
                {"months": 3, "en": "Months 4–6 · Upper-intermediate", "bn": "৪–৬ মাস · আপার-ইন্টারমিডিয়েট",
                 "levels": [5, 6], "topics": [], "bands": ["medium"], "pron": ["medium"], "words": ("core7000", 53, 78)},
                {"months": 3, "en": "Months 7–9 · Band 6.5 and above", "bn": "৭–৯ মাস · ব্যান্ড ৬.৫ ও তার বেশি",
                 "levels": [7, 8], "topics": [], "bands": ["advanced"], "pron": ["advanced"], "words": ("core7000", 79, 104)},
            ],
            12: [
                {"months": 4, "en": "Months 1–4 · Strong foundations", "bn": "১–৪ মাস · মজবুত ভিত্তি",
                 "levels": [2, 3, 4], "topics": [], "bands": ["easy"], "pron": ["easy"], "words": ("core7000", 1, 35)},
                {"months": 4, "en": "Months 5–8 · Upper-intermediate", "bn": "৫–৮ মাস · আপার-ইন্টারমিডিয়েট",
                 "levels": [5, 6], "topics": [], "bands": ["medium"], "pron": ["medium"], "words": ("core7000", 36, 70)},
                {"months": 4, "en": "Months 9–12 · Band 6.5 and above", "bn": "৯–১২ মাস · ব্যান্ড ৬.৫ ও তার বেশি",
                 "levels": [7, 8], "topics": [], "bands": ["advanced"], "pron": ["advanced"], "words": ("core7000", 71, 104)},
            ],
        },
    },
    "adult": {
        "years": 1, "en": "Parent who studied at school or college", "bn": "স্কুল/কলেজে পড়া অভিভাবক",
        "why_en": "You know some English already; one year makes it spoken English you can teach at home. "
                  "It is the busiest course: plan 30 minutes a day.",
        "why_bn": "আপনি কিছু ইংরেজি জানেন; এক বছরে তা মুখের ইংরেজি হবে, যা বাসায় শেখাতে পারবেন। "
                  "এটি সবচেয়ে ঘন কোর্স: দিনে ৩০ মিনিট রাখুন।",
        "stages": [
            {"months": 3, "en": "Months 1–3 · Sounds you will teach your child", "bn": "১–৩ মাস · যে ধ্বনিগুলো সন্তানকে শেখাবেন",
             "levels": [0], "topics": ["daily"], "bands": [], "pron": ["easy"], "words": ("kids3000", 1, 39)},
            {"months": 5, "en": "Months 4–8 · Everyday English", "bn": "৪–৮ মাস · প্রতিদিনের ইংরেজি",
             "levels": [3, 4, 5, 6], "topics": ["study"], "bands": ["easy", "medium"], "pron": ["medium"], "words": ("kids3000", 40, 104)},
            {"months": 4, "en": "Months 9–12 · Fluent English", "bn": "৯–১২ মাস · সাবলীল ইংরেজি",
             "levels": [7, 8], "topics": ["trip"], "bands": ["advanced"], "pron": ["advanced"], "words": ("kids3000", 105, 156)},
        ],
    },
    "elder": {
        "years": 3, "en": "Grandparent or adult who studied little", "bn": "দাদা-দাদি বা কম পড়াশোনা করা বড়রা",
        "why_en": "Starting from the letters is fine. Slow, steady practice with the grandchildren works.",
        "why_bn": "অক্ষর থেকে শুরু করা কোনো সমস্যা নয়। নাতি-নাতনিদের সাথে ধীরে ধীরে নিয়মিত চর্চাই কাজ করে।",
        "stages": [
            {"months": 12, "en": "Year 1 · Letters, sounds and greetings", "bn": "১ম বছর · অক্ষর, ধ্বনি ও সম্ভাষণ",
             "levels": [0, 1], "topics": ["daily"], "bands": [], "pron": [], "words": ("kids3000", 1, 52)},
            {"months": 12, "en": "Year 2 · Reading and daily talk", "bn": "২য় বছর · পড়া ও প্রতিদিনের কথা",
             "levels": [2, 3, 4, 5], "topics": ["study"], "bands": [], "pron": ["easy"], "words": ("kids3000", 53, 104)},
            {"months": 12, "en": "Year 3 · Speaking with the family", "bn": "৩য় বছর · পরিবারের সাথে কথা বলা",
             "levels": [6, 7, 8], "topics": ["trip"], "bands": ["easy"], "pron": ["medium"], "words": ("kids3000", 105, 156)},
        ],
    },
}


def stage_items(stage):
    """New items of a stage, mixed so that lessons, talks, course, pronunciation and word weeks alternate."""
    from course.models import CourseLesson
    from practice.models import VocabDeck

    lessons = list(Lesson.objects.filter(module__level__number__in=stage["levels"])
                   .order_by("module__level__number", "module__order", "order"))
    topics = list(TalkTopic.objects.filter(group__in=stage["topics"]).order_by("group", "order"))
    course = [c for band in stage["bands"]
              for c in sorted(CourseLesson.objects.filter(band=band).exclude(slug__startswith="pr-"),
                              key=lambda c: (c.order, c.skill))]
    pron = [c for band in stage.get("pron", [])
            for c in CourseLesson.objects.filter(band=band, slug__startswith="pr-").order_by("order")]
    words = []
    if stage.get("words"):
        series, a, b = stage["words"]
        words = list(VocabDeck.objects.filter(series=series, week__gte=a, week__lte=b).order_by("week"))
    streams = [s for s in (lessons, topics, course, pron, words) if s]
    total = sum(len(s) for s in streams)
    # Proportional merge: always take from the stream that is furthest behind its share.
    taken = [0] * len(streams)
    out = []
    for _ in range(total):
        i = min((i for i in range(len(streams)) if taken[i] < len(streams[i])),
                key=lambda i: (taken[i] + 1) / len(streams[i]))
        out.append(streams[i][taken[i]])
        taken[i] += 1
    return out


def _kind(item):
    from course.models import CourseLesson
    from practice.models import VocabDeck
    if isinstance(item, CourseLesson):
        return "course"
    if isinstance(item, VocabDeck):
        return "words"
    return "topic" if isinstance(item, TalkTopic) else "lesson"


def _day(plan, date, item, kind, stage):
    row = PlanDay(plan=plan, date=date, kind=kind, stage=stage)
    if isinstance(item, Lesson):
        row.lesson = item
    elif isinstance(item, TalkTopic):
        row.topic = item
    elif _kind(item) == "words":
        row.deck = item
    else:
        row.course_lesson = item
    return row


def schedule(plan, dates, items, stage):
    """New items spread evenly over the dates; the other dates repeat earlier items."""
    rows = []
    if not dates or not items:
        return rows
    n_days, n_items = len(dates), len(items)
    if n_items >= n_days:
        cap = int(n_days * MAX_PER_DAY)
        for i, item in enumerate(items[:cap]):
            rows.append(_day(plan, dates[i * n_days // len(items[:cap])], item, _kind(item), stage))
        return rows
    first_day = {i * n_days // n_items: items[i] for i in range(n_items)}
    seen, repeated_once, pointer = [], set(), 0
    for d_i, date in enumerate(dates):
        if d_i in first_day:
            item = first_day[d_i]
            seen.append(item)
            rows.append(_day(plan, date, item, _kind(item), stage))
            continue
        if not seen:
            continue
        last = seen[-1]
        if id(last) not in repeated_once:          # repeat yesterday's new item first
            repeated_once.add(id(last))
            item = last
        else:                                      # then walk back through everything learned
            item = seen[pointer % len(seen)]
            pointer += 1
        rows.append(_day(plan, date, item, "review", stage))
    return rows


def recommend_months(learner):
    """IELTS length from the latest level test (overall level 0–8): strong learners need less time."""
    test = learner.smart_tests.filter(finished_at__isnull=False).first() if hasattr(learner, "smart_tests") else None
    if not test:
        return 12
    level = test.overall()
    return 3 if level >= 6 else 6 if level == 5 else 9 if level == 4 else 12


def stages_of(track, months=None):
    spec = TRACKS[track]
    if spec.get("variants"):
        months = months if months in spec["variants"] else 12
        return spec["variants"][months]
    return spec["stages"]


def length_months(track, months=None):
    return sum(s["months"] for s in stages_of(track, months))


@transaction.atomic
def build_track_plan(learner, track, days_per_week=5, minutes_per_day=20, start=None, months=None):
    from django.utils import timezone

    if TRACKS[track].get("variants") and months is None:
        months = recommend_months(learner)
    stages = stages_of(track, months)
    total = length_months(track, months)
    start = start or timezone.localdate()
    end = add_months(start, total)
    StudyPlan.objects.filter(learner=learner, is_active=True).update(is_active=False)
    first_levels = [lv for st in stages for lv in st["levels"]] or [0]
    plan = StudyPlan.objects.create(
        learner=learner, kind="track", track=track,
        start_level=min(first_levels), target_level=8, months=total,
        days_per_week=days_per_week, minutes_per_day=minutes_per_day, start_date=start, end_date=end)
    rows, s_start = [], start
    for stage in stages:
        s_end = add_months(s_start, stage["months"])
        rows += schedule(plan, list(study_dates(s_start, s_end, days_per_week)), stage_items(stage), stage["en"])
        d = s_start
        while d < s_end:
            if d.weekday() == FRIDAY:
                rows.append(PlanDay(plan=plan, date=d, kind="family", stage=stage["en"]))
            d += timedelta(days=1)
        s_start = s_end
    PlanDay.objects.bulk_create(rows)
    if learner.track != track:
        learner.track = track
        learner.save(update_fields=["track"])
    return plan


def summary(track, months=None):
    """Numbers for the plan page: new lessons per stage."""
    return [{"en": s["en"], "bn": s["bn"], "months": s["months"], "new": len(stage_items(s))}
            for s in stages_of(track, months)]
