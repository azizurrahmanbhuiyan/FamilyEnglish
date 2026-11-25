from . import grammar, handbook, listening, pronunciation, reading, speaking, writing

MODULES = [listening, speaking, reading, writing, grammar, pronunciation, handbook]


def all_lessons():
    """Yield (skill, lesson_dict) for every lesson in the course."""
    for mod in MODULES:
        for lesson in mod.LESSONS:
            yield mod.SKILL, lesson
    for skill, lesson in handbook.EXTRA:
        yield skill, lesson
