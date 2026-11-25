"""'Talk at home': two short lines for each family member in every kids' lesson.

Me & Sister, Me & Brother, Me & Mamma, Me & Daddy, Me & Grandma, Me & Grandpa.
The child says the first line; the family member answers with the second. Families can
ask the AI for a fresh set of sentences for a lesson (saved for that family only).
"""

import json

MEMBERS = [
    ("sister", "Sister", "বোন", "👧"),
    ("brother", "Brother", "ভাই", "👦"),
    ("mamma", "Mamma", "আম্মু", "👩"),
    ("daddy", "Daddy", "আব্বু", "👨"),
    ("grandma", "Grandma", "দাদি / নানি", "👵"),
    ("grandpa", "Grandpa", "দাদা / নানা", "👴"),
]
MEMBER_KEYS = [m[0] for m in MEMBERS]
MEMBER_INFO = {k: {"key": k, "name": n, "bn": bn, "emoji": e} for k, n, bn, e in MEMBERS}
TALK_XP = 5


def from_tuples(rows):
    """Seed format (me, them, me_bn, them_bn) x 6 -> stored JSON list."""
    return [{"who": who, "me": me, "them": them, "me_bn": me_bn, "them_bn": them_bn}
            for who, (me, them, me_bn, them_bn) in zip(MEMBER_KEYS, rows)]


def cards(data):
    """Talk data joined with the member names, in the fixed family order."""
    by_who = {d.get("who"): d for d in data or []}
    out = []
    for key in MEMBER_KEYS:
        d = by_who.get(key)
        if d and d.get("me") and d.get("them"):
            out.append({**MEMBER_INFO[key], **d})
    return out


def talk_for(item, family=None, original=False):
    """The family's AI set for this lesson/topic if there is one (unless original=True), else the built-in set."""
    if family is not None and not original:
        custom = item.talk_sets.filter(family=family).first()
        if custom and custom.data:
            return cards(custom.data), custom
    return cards(item.family_talk), None


def _clean(text, limit=120):
    return " ".join(str(text or "").split())[:limit]


def ai_generate(lesson, learner=None, topic=None):
    """Ask the AI for 6 new two-line talks for a lesson (or a theme topic). Returns the list or None."""
    from practice import ai

    age = learner.age if learner else None
    if topic is not None:
        about = (f"Theme: {topic.title} ({topic.get_group_display()}). Useful words: "
                 + ", ".join(w["word"] for w in topic.words) + ". Simple level for children and parents.")
    else:
        about = (f"Level {lesson.module.level.number} of 0-8. Lesson: {lesson.title}. Focus: {lesson.focus}.")
    reply = ai.ask(
        "You write tiny everyday English conversations for a Bangladeshi family learning English at home. "
        "For each family member (sister, brother, mamma, daddy, grandma, grandpa) write exactly 2 short "
        "lines: 'me' = what the child says, 'them' = what that family member answers. Use the lesson's "
        "sound, words or grammar naturally, everyday home life (food, school, prayer time, rickshaw, rain, "
        "games), warm and polite, no names of real people. Keep each line under 10 words for levels 0-2 and "
        "under 14 words above that. Add simple Bangla translations. Reply ONLY with JSON: "
        '[{"who": "sister", "me": "...", "them": "...", "me_bn": "...", "them_bn": "..."}, ...] in the order '
        "sister, brother, mamma, daddy, grandma, grandpa.",
        [{"role": "user", "content": f"{about} Child's age: {age or 'unknown'}."}],
        max_tokens=1200)
    if not reply:
        return None
    try:
        data = json.loads(reply[reply.find("["): reply.rfind("]") + 1])
    except ValueError:
        return None
    out = []
    for d in data if isinstance(data, list) else []:
        if isinstance(d, dict) and d.get("who") in MEMBER_KEYS and d.get("me") and d.get("them"):
            out.append({"who": d["who"], "me": _clean(d["me"]), "them": _clean(d["them"]),
                        "me_bn": _clean(d.get("me_bn"), 200), "them_bn": _clean(d.get("them_bn"), 200)})
    return out if len({d["who"] for d in out}) == 6 else None


def said_keys(learner, lesson=None, topic=None):
    """Which members' talks this learner has already ticked for this lesson or theme topic."""
    prefix = f"topic-{topic.pk}-" if topic is not None else f"talk-{lesson.pk}-"
    return {k[len(prefix):] for k in learner.xp_events.filter(key__startswith=prefix).values_list("key", flat=True)}
