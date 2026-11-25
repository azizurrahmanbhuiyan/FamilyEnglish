"""Organise lessons from the AI level test results.

Rules
- Each skill starts in the category the test found (Easy / Medium / Advanced) and then moves up.
  Lessons below the starting category stay open in the library but are not in the path.
- The weakest skill comes first and gets two lessons for every one lesson of the other skills, so it
  catches up. The second-weakest gets 1.5 (it appears three times in every two rounds).
- Lessons already passed are left out.
"""

from .models import BAND_ORDER, COURSE_SKILLS, CourseLesson, CourseProgress, band_of_level

WEIGHTS = [2.0, 1.5, 1.0, 1.0, 1.0]


def start_bands(learner):
    """Starting category per skill: latest AI test, else the latest placement, else Easy."""
    test = learner.smart_tests.filter(finished_at__isnull=False).first()
    if test and test.bands:
        return dict(test.bands), dict(test.levels), test
    p = learner.placements.first()
    if p:
        lv = p.skill_levels()
        lv["grammar"] = lv.get("writing", 0)
        return {k: band_of_level(v).value for k, v in lv.items()}, lv, None
    return {k: "easy" for k in COURSE_SKILLS}, {k: 0 for k in COURSE_SKILLS}, None


def build_path(learner, limit=None):
    bands, levels, _ = start_bands(learner)
    passed = set(CourseProgress.objects.filter(learner=learner, passed=True).values_list("lesson_id", flat=True))
    queues = {}
    for skill in COURSE_SKILLS:
        first = BAND_ORDER.index(bands.get(skill, "easy"))
        allowed = [b.value for b in BAND_ORDER[first:]]
        qs = CourseLesson.objects.filter(skill=skill, band__in=allowed)
        queues[skill] = sorted((l for l in qs if l.id not in passed),
                               key=lambda l: (BAND_ORDER.index(l.band), l.order))
    order = sorted(COURSE_SKILLS, key=lambda s: (levels.get(s, 0), COURSE_SKILLS.index(s)))
    credit = {s: 0.0 for s in order}
    path = []
    while any(queues.values()):
        for i, skill in enumerate(order):
            credit[skill] += WEIGHTS[i]
            while credit[skill] >= 1 and queues[skill]:
                path.append(queues[skill].pop(0))
                credit[skill] -= 1
        if limit and len(path) >= limit:
            return path[:limit]
    return path


def why_text(lesson, learner, lang="en"):
    """One line that explains why this lesson is next ('Why this task today?')."""
    bands, levels, test = start_bands(learner)
    weakest = min(levels, key=lambda k: (levels[k], COURSE_SKILLS.index(k))) if levels else None
    src_en = "your AI level test" if test else "your placement test"
    src_bn = "AI লেভেল টেস্ট" if test else "প্লেসমেন্ট টেস্ট"
    if lesson.skill == weakest:
        return (f"{lesson.skill_bn} আপনার সবচেয়ে দুর্বল দক্ষতা ({src_bn} অনুযায়ী), তাই এটি বেশি রাখা হয়েছে। "
                f"আজ: {lesson.band_bn} স্তরের \"{lesson.title}\"।" if lang == "bn" else
                f"{lesson.get_skill_display()} is your weakest skill in {src_en}, so it comes up more often. "
                f"Today: {lesson.get_band_display()} lesson \"{lesson.title}\".")
    return (f"{src_bn} অনুযায়ী আপনার {lesson.skill_bn} {lesson.band_bn} স্তরে; ধাপে ধাপে এগোতে আজ \"{lesson.title}\"।"
            if lang == "bn" else
            f"{src_en.capitalize()} placed your {lesson.get_skill_display()} at {lesson.get_band_display()}. "
            f"\"{lesson.title}\" is the next step.")
