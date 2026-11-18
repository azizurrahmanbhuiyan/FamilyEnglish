"""Placement scoring.

Young children (under 7 or non-readers) take a short tap game: phonics questions for
Levels 0-2. Readers take one question per level (3-8) in Listening, Reading and
Writing, plus a can-do checklist for Speaking (answered by the parent or the adult
learner). AI speaking/writing marking can replace the checklist later (see README).
"""

from .models import Placement, PlacementQuestion, Skill

READER_SKILLS = [Skill.LISTENING, Skill.READING, Skill.WRITING]
READER_MIN, READER_MAX = 3, 8

# Can-do statements for speaking, one per level (3-8)
SPEAKING_CAN_DO = [
    (3, "Can say their name, age and name everyday things (\"It's a cat\")."),
    (4, "Can talk about their daily routine in short sentences."),
    (5, "Can tell what happened yesterday, using the past tense."),
    (6, "Can keep a simple conversation going and give opinions with reasons."),
    (7, "Can discuss a topic in detail and argue a point of view."),
    (8, "Can present and debate fluently on complex topics."),
]


def score_ladder(correct_by_level: dict, floor: int, ceiling: int, allowed_misses: int = 1) -> int:
    """Climb levels in order; stop after more than `allowed_misses` misses.

    Returns the highest level reached, or `floor - 1` if the first level is missed
    twice. For readers floor=3, so an empty result gives Level 2 (Phonics Complete).
    """
    level, misses = floor - 1, 0
    for lv in range(floor, ceiling + 1):
        if correct_by_level.get(lv):
            level = lv
        else:
            misses += 1
            if misses > allowed_misses:
                break
    return level


def score_young_child(answers: dict) -> int:
    """answers: {question_id: chosen}. Level = highest phonics level with >= 2/3 correct."""
    qs = PlacementQuestion.objects.filter(skill=Skill.PHONICS, level__lte=2)
    by_level = {}
    for q in qs:
        ok = answers.get(str(q.id), "").strip().lower() == q.answer.strip().lower()
        right, total = by_level.get(q.level, (0, 0))
        by_level[q.level] = (right + ok, total + 1)
    # Passing the Level 0 questions means ready for Level 1, and so on, up to Level 3.
    level = 0
    for lv in (0, 1, 2):
        right, total = by_level.get(lv, (0, 0))
        if total and right / total >= 2 / 3:
            level = lv + 1
        else:
            break
    return level


def score_reader(answers: dict, speaking_level: int):
    result = {}
    for skill in READER_SKILLS:
        correct_by_level = {}
        for q in PlacementQuestion.objects.filter(skill=skill, level__gte=READER_MIN,
                                                  level__lte=READER_MAX):
            ok = answers.get(str(q.id), "").strip().lower() == q.answer.strip().lower()
            # a level counts as passed if every question at that level is right
            correct_by_level[q.level] = correct_by_level.get(q.level, True) and ok
        result[skill.value] = score_ladder(correct_by_level, READER_MIN, READER_MAX)
    result[Skill.SPEAKING.value] = max(2, min(speaking_level, READER_MAX))
    return result


def save_placement(learner, levels: dict, young=False) -> Placement:
    overall = round(sum(levels.values()) / len(levels))
    return Placement.objects.create(
        learner=learner, young_child_test=young, overall=overall, **levels)
