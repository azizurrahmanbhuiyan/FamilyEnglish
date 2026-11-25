"""AI level test: Listening, Reading, Grammar, Writing and Speaking.

How it works
1. Listening, Reading and Grammar start with Easy + Medium questions. Only learners who pass
   the Medium questions get the extra Advanced questions (adaptive).
2. Writing and Speaking are marked by the AI coach with a rubric (FE_AI_TEST_MODEL, a stronger
   model by default). Without an AI key the built-in rubric marks them: length, sentence length,
   linking words, word variety, mistakes found by the checker, and how well sentences were repeated.
3. The results give a level (0-8) and a category (Easy / Medium / Advanced) for each skill, and the
   AI writes a personal report. course.path then orders the lessons from these results.
"""

import json
import re
from statistics import mean

from django.conf import settings
from django.utils import timezone

from practice import ai
from practice.feedback import check_writing, speaking_score

from .content._h import C
from .grading import normalize
from .models import AnswerLog, SmartTest, band_of_level

OBJECTIVE = ["listening", "reading", "grammar"]
FIRST_STEPS = ["listening:1", "reading:1", "grammar:1", "writing:1", "speaking:1"]

LISTENING = {
    "easy": [
        C("What does the girl want?", "a glass of water", "a glass of milk", "a cup of tea",
          say="Can I have a glass of water, please?", qt="lis_detail"),
        C("How old is the boy?", "eleven", "seven", "seventeen", say="My brother is eleven years old.",
          qt="lis_number"),
        C("Where is the key?", "on the table", "under the table", "in the bag",
          say="Your key is on the table.", qt="lis_detail"),
    ],
    "medium": [
        C("When does the bus leave?", "at quarter to eight", "at quarter past eight", "at eight",
          say="Hurry up! The bus leaves at quarter to eight.", qt="lis_number"),
        C("Why is the shop closed?", "the owner is ill", "it is a holiday", "it is too late",
          say="Sorry, the shop is closed today because the owner is ill.", qt="lis_detail"),
        C("What will they do on Friday?", "visit their aunt", "go shopping", "stay at home",
          say="We can't come on Friday. We're going to visit our aunt in Barishal.", qt="lis_detail"),
    ],
    "advanced": [
        C("What is the speaker's main point?", "Online classes help, but children still need teachers.",
          "Online classes are useless.", "Teachers should use more phones.",
          say="Online classes have clearly helped many families. However, my view is that young children "
              "still learn best with a teacher in the room, especially for speaking.", qt="lis_gist"),
        C("How does the speaker feel about the new road?", "disappointed", "excited", "not sure",
          say="They promised the new road would be finished by June. It's now December, and honestly, "
              "nothing much has changed.", qt="lis_attitude"),
        C("What happened as a result of the rain?", "the exam was postponed", "the school closed for a week",
          "students stayed late", say="Due to heavy rain across the city, this morning's exam has been "
                                      "postponed until next Tuesday.", qt="lis_detail"),
    ],
}

READING = {
    "easy": {
        "passage": "Sami has a small garden. He grows tomatoes and chillies. Every morning he waters the "
                   "plants before school. His grandmother helps him on Fridays.",
        "items": [
            C("What does Sami grow?", "tomatoes and chillies", "mangoes", "flowers", qt="rd_detail"),
            C("When does he water the plants?", "every morning", "every evening", "on Fridays", qt="rd_detail"),
            C("Who helps him?", "his grandmother", "his teacher", "his sister", qt="rd_detail"),
        ],
    },
    "medium": {
        "passage": "Our town's new market opened last month. It is cleaner than the old one and has a "
                   "roof, so people can shop even in the rain. Some sellers are unhappy because the rent "
                   "is higher. However, most customers say they prefer it.",
        "items": [
            C("Why can people shop in the rain?", "it has a roof", "it is cleaner", "it is new", qt="rd_detail"),
            C("Why are some sellers unhappy?", "the rent is higher", "there are no customers",
              "it is too far", qt="rd_detail"),
            C("What do most customers think?", "they prefer the new market", "they prefer the old market",
              "they don't care", qt="rd_gist"),
        ],
    },
    "advanced": {
        "passage": "Although solar panels were once considered a luxury, falling prices have made them a "
                   "practical choice for many rural households. Families that previously relied on "
                   "kerosene lamps now light their homes cheaply, and children can study after dark. "
                   "Critics point out, however, that old batteries are rarely recycled properly, which "
                   "could create a new environmental problem.",
        "items": [
            C("What made solar panels practical?", "lower prices", "government rules", "better weather",
              qt="rd_detail"),
            C("'previously relied on' means families…", "used to depend on", "never used", "sold",
              qt="rd_vocab"),
            C("What is the critics' concern?", "battery waste", "high prices", "children studying too late",
              qt="rd_infer"),
        ],
    },
}

GRAMMAR = {
    "easy": [
        C("She ___ a doctor.", "is", "are", "am", qt="gr_be"),
        C("I have ___ orange.", "an", "a", "the", qt="gr_articles"),
        C("My father ___ to work by bus.", "goes", "go", "going", qt="gr_tense"),
    ],
    "medium": [
        C("We ___ to Sylhet last winter.", "went", "go", "have gone", qt="gr_tense"),
        C("This box is ___ than that one.", "heavier", "more heavy", "heaviest", qt="gr_compare"),
        C("How ___ money do you need?", "much", "many", "few", qt="gr_quantity"),
    ],
    "advanced": [
        C("I ___ here since 2019.", "have lived", "live", "am living", qt="gr_tense"),
        C("If I ___ more time, I would learn to paint.", "had", "have", "will have", qt="gr_condition"),
        C("The bridge ___ in 2022.", "was opened", "opened by", "is open", qt="gr_passive"),
    ],
}

LINKERS = ["because", "but", "so", "however", "although", "moreover", "therefore", "first", "then",
           "finally", "also", "for example", "for instance", "while", "after that", "in addition",
           "on the other hand", "as a result", "in my opinion", "i think"]


def writing_task(learner):
    age = learner.age
    if learner.role == "child" and age is not None and age <= 9:
        return {"q": "Write 3 to 5 sentences about your family or your best friend.", "min": 15}
    if learner.role == "child":
        return {"q": "Write about a place you like to visit. Say where it is, what you do there and why "
                     "you like it.", "min": 50}
    return {"q": "Some people say parents should learn English together with their children at home. "
                 "Do you agree? Give your reasons and an example. (80–120 words)", "min": 80}


def speaking_tasks(learner):
    young = learner.role == "child"
    return {
        "repeat": ["I go to school by rickshaw every morning.",
                   "Could you tell me how to get to the nearest hospital, please?"],
        "open": ("Tell me about your favourite game or toy. Why do you like it?" if young else
                 "Describe a person who helped you learn something important. What did they teach you, "
                 "and how?"),
        "min": 20 if young else 45,
    }


# ------------------------------------------------------------------ steps

def items_for(step_key):
    skill, part = step_key.split(":")
    bank = {"listening": LISTENING, "grammar": GRAMMAR}.get(skill)
    if bank:
        return bank["easy"] + bank["medium"] if part == "1" else bank["advanced"]
    if skill == "reading":
        if part == "1":
            return READING["easy"]["items"] + READING["medium"]["items"]
        return READING["advanced"]["items"]
    return []


def passages_for(step_key):
    skill, part = step_key.split(":")
    if skill != "reading":
        return []
    keys = ["easy", "medium"] if part == "1" else ["advanced"]
    return [{"text": READING[k]["passage"], "items": len(READING[k]["items"])} for k in keys]


def start(learner):
    return SmartTest.objects.create(learner=learner, steps=list(FIRST_STEPS))


def current_step(test):
    return test.steps[test.step] if test.step < len(test.steps) else None


def submit_objective(test, step_key, data):
    """Mark one Listening/Reading/Grammar step. Adds the Advanced step if Medium was passed."""
    items = items_for(step_key)
    marks = []
    for i, it in enumerate(items):
        given = (data.get(f"q{i}") or "").strip()
        ok = normalize(given) == normalize(it["a"])
        marks.append(ok)
        AnswerLog.objects.create(learner=test.learner, skill=step_key.split(":")[0], qtype=it["qt"],
                                 source="smart", correct=ok, given=given[:300], expected=it["a"][:300])
    test.answers[step_key] = marks
    skill, part = step_key.split(":")
    if part == "1" and sum(marks[3:6]) >= 2:
        test.steps.insert(test.step + 1, f"{skill}:2")
    test.step += 1
    test.save()


def submit_writing(test, text):
    test.answers["writing"] = (text or "").strip()[:3000]
    test.step += 1
    test.save()


def submit_speaking(test, repeats, open_answer, typed=False):
    test.answers["speaking"] = {"repeats": [(r or "")[:500] for r in repeats],
                                "open": (open_answer or "")[:3000], "typed": bool(typed)}
    test.step += 1
    test.save()


# ------------------------------------------------------------------ scoring

def objective_level(marks1, marks2=None):
    easy, med = sum(marks1[:3]), sum(marks1[3:6])
    if easy < 2:
        return 1 if easy == 0 else 2
    if med < 2:
        return 3
    if marks2 is None or sum(marks2) < 2:
        return 4 if med == 2 else 5
    return 7 if sum(marks2) == 2 else 8


def _sentences(text):
    return [s for s in re.split(r"[.!?]+", text) if s.strip()]


def _linkers(text):
    t = f" {text.lower()} "
    return sum(1 for k in LINKERS if f" {k} " in t or f" {k}," in t)


def rule_writing_level(text, min_words):
    words = re.findall(r"[A-Za-z']+", text)
    n = len(words)
    if n == 0:
        return 0, {}
    sents = _sentences(text) or [text]
    avg = n / len(sents)
    _, notes = check_writing(text)
    long_ratio = sum(1 for w in words if len(w) >= 7) / n
    variety = len({w.lower() for w in words}) / n
    pts = (0 if n < 10 else 1 if n < 25 else 2 if n < 50 else 3 if n < 80 else 4)
    pts += 0 if avg < 5 else 1 if avg < 9 else 2 if avg < 15 else 3
    link = _linkers(text)
    pts += 0 if link == 0 else 1 if link <= 2 else 2 if link <= 4 else 3
    pts += 0 if long_ratio < 0.08 else 1 if long_ratio < 0.15 else 2
    penalty = min(3, len(notes)) * 0.75 + (1 if variety < 0.45 and n > 20 else 0)
    if n < min_words * 0.5:
        penalty += 1
    level = max(1, min(8, 1 + round((pts - penalty) * 7 / 12)))
    return level, {"words": n, "avg_sentence": round(avg, 1), "linkers": link, "notes": notes[:5]}


def rule_speaking_level(repeats_heard, repeats_target, open_answer, min_words):
    sims = [speaking_score(t, h) for t, h in zip(repeats_target, repeats_heard)]
    rep = mean(sims) if sims else 0
    w = len(open_answer.split())
    link = _linkers(open_answer)
    if rep < 40 and w < 5:
        level = 1
    elif rep < 60:
        level = 2
    elif w < 10:
        level = 3
    elif w < 25:
        level = 4
    elif w < 45:
        level = 5
    elif link < 2:
        level = 6
    elif w < 70:
        level = 7
    else:
        level = 8
    return level, {"repeat_accuracy": round(rep), "words": w, "linkers": link}


def _ask_json(system, content, max_tokens=700):
    reply = ai.ask(system, [{"role": "user", "content": content}], max_tokens=max_tokens,
                   model=getattr(settings, "AI_TEST_MODEL", None))
    if not reply:
        return None
    try:
        return json.loads(reply[reply.find("{"): reply.rfind("}") + 1])
    except ValueError:
        return None


RUBRIC = ("Levels: 0-2 = beginner (single words, phonics), 3 = simple sentences (Pre A1/A1), "
          "4 = A1/A2 short connected sentences, 5 = A2/B1 paragraphs with some errors, "
          "6 = B1/B2 clear organised text with linking, 7 = B2/C1 wide range and few errors, "
          "8 = C1+ fluent, precise and natural.")


def ai_writing(task, text, learner):
    return _ask_json(
        "You are an experienced English examiner marking a placement test for FamilyEnglish, a "
        "Bangladeshi family learning site. " + RUBRIC + " Consider task response, organisation, "
        "vocabulary range and grammar accuracy. Reply ONLY with JSON: {\"level\": 0-8, "
        "\"strengths\": [\"…\"], \"fixes\": [{\"wrong\": \"…\", \"right\": \"…\", \"why_bn\": \"…\"}], "
        "\"comment_bn\": \"<2 sentences in Bangla for the learner>\"}. Max 3 strengths, max 4 fixes.",
        f"Learner: {learner.get_role_display()}, age {learner.age or 'unknown'}.\nTask: {task}\nAnswer:\n{text}")


def ai_speaking(task, transcript, repeat_acc, learner):
    return _ask_json(
        "You are an experienced English speaking examiner. You get a speech-to-text transcript, so ignore "
        "punctuation and small recognition errors; judge range, grammar, coherence and how much the learner "
        "could say. The repeat-accuracy number shows how well they repeated model sentences "
        "(pronunciation clue). " + RUBRIC + " Reply ONLY with JSON: {\"level\": 0-8, \"strengths\": [\"…\"], "
        "\"fixes\": [{\"wrong\": \"…\", \"right\": \"…\", \"why_bn\": \"…\"}], \"comment_bn\": \"…\"}.",
        f"Learner: {learner.get_role_display()}, age {learner.age or 'unknown'}.\nQuestion: {task}\n"
        f"Repeat accuracy: {repeat_acc}%\nTranscript: {transcript}")


def ai_report(test, mistakes):
    return _ask_json(
        "You are a kind, practical English coach writing a placement report for a Bangladeshi family. "
        "Reply ONLY with JSON: {\"summary_bn\": \"<3 sentences in Bangla>\", \"summary_en\": \"<2 short "
        "sentences in simple English>\", \"strengths\": [\"…\"], \"focus\": [\"…\"], \"tips\": [\"<practical "
        "home activity>\", …]}. Max 3 items in each list. Mention the weakest skill first in focus.",
        f"Levels (0-8): {json.dumps(test.levels)}\nCategories: {json.dumps(test.bands)}\n"
        f"Question types answered wrongly: {', '.join(mistakes) or 'none'}\n"
        f"Writing notes: {json.dumps(test.scores.get('writing', {}))[:600]}\n"
        f"Speaking notes: {json.dumps(test.scores.get('speaking', {}))[:600]}", max_tokens=900)


def finish(test):
    """Work out levels and categories, write the report, save a Placement."""
    from learning.models import Placement
    from .qtypes import label

    learner = test.learner
    levels, scores = {}, {}
    for skill in OBJECTIVE:
        m1 = test.answers.get(f"{skill}:1", [False] * 6)
        m2 = test.answers.get(f"{skill}:2")
        levels[skill] = objective_level(m1, m2)
        scores[skill] = {"right": sum(m1) + sum(m2 or []), "total": len(m1) + len(m2 or []),
                         "advanced_round": m2 is not None}

    task = writing_task(learner)
    text = test.answers.get("writing", "")
    w_level, w_info = rule_writing_level(text, task["min"])
    used_ai = False
    if text and ai.enabled():
        res = ai_writing(task["q"], text, learner)
        if res and isinstance(res.get("level"), (int, float)):
            w_level = max(0, min(8, int(res["level"])))
            w_info.update(strengths=res.get("strengths", [])[:3], fixes=res.get("fixes", [])[:4],
                          comment_bn=res.get("comment_bn", ""), ai=True)
            used_ai = True
    levels["writing"], scores["writing"] = w_level, w_info

    sp = speaking_tasks(learner)
    spd = test.answers.get("speaking", {"repeats": [], "open": ""})
    s_level, s_info = rule_speaking_level(spd.get("repeats", []), sp["repeat"], spd.get("open", ""), sp["min"])
    if spd.get("open") and ai.enabled():
        res = ai_speaking(sp["open"], spd["open"], s_info["repeat_accuracy"], learner)
        if res and isinstance(res.get("level"), (int, float)):
            ai_level = max(0, min(8, int(res["level"])))
            if s_info["repeat_accuracy"] < 50:
                ai_level = min(ai_level, 4)
            s_level = round((ai_level * 2 + s_level) / 3)
            s_info.update(strengths=res.get("strengths", [])[:3], fixes=res.get("fixes", [])[:4],
                          comment_bn=res.get("comment_bn", ""), ai=True)
            used_ai = True
    if spd.get("typed"):
        s_info["typed"] = True
    levels["speaking"], scores["speaking"] = s_level, s_info

    test.levels = levels
    test.bands = {k: band_of_level(v).value for k, v in levels.items()}
    test.scores = scores
    wrong = (AnswerLog.objects.filter(learner=learner, source="smart", correct=False,
                                      created_at__gte=test.started_at).values_list("qtype", flat=True))
    mistakes = sorted({label(q) for q in wrong})
    report = ai_report(test, mistakes) if ai.enabled() else None
    if report:
        used_ai = True
    test.report = report or rule_report(test, mistakes)
    test.ai_used = used_ai
    test.finished_at = timezone.now()
    test.save()

    four = {k: levels[k] for k in ("listening", "speaking", "reading", "writing")}
    Placement.objects.create(learner=learner, overall=round(sum(four.values()) / 4), **four)
    return test


SKILL_TIPS = {
    "listening": "প্রতিদিন ১০ মিনিট BBC Learning English বা British Council-এর ছোট অডিও শুনুন, তারপর যা শুনলেন তা বাংলায় বলুন।",
    "speaking": "রাতের খাবারের সময় পরিবারে ৫ মিনিট শুধু ইংরেজিতে কথা বলুন — আজকের দিন কেমন গেল।",
    "reading": "প্রতিদিন একটি ছোট গল্প বা খবর জোরে পড়ুন, অজানা শব্দ খাতায় লিখুন।",
    "writing": "প্রতিদিন ৩–৫ বাক্যের ডায়েরি লিখুন, তারপর Writing helper দিয়ে যাচাই করুন।",
    "grammar": "প্রতিদিন একটি grammar lesson শেষ করে self-test দিন; ভুলগুলো আবার করুন।",
}


def rule_report(test, mistakes):
    names = {"listening": "Listening", "speaking": "Speaking", "reading": "Reading", "writing": "Writing",
             "grammar": "Grammar"}
    order = sorted(test.levels, key=lambda k: test.levels[k])
    weak, strong = order[0], order[-1]
    return {
        "summary_en": f"Your strongest skill is {names[strong]}. Start with {names[weak]} — your course puts "
                      f"those lessons first.",
        "summary_bn": f"আপনার সবচেয়ে ভালো দক্ষতা {names[strong]} (লেভেল {test.levels[strong]})। "
                      f"{names[weak]} (লেভেল {test.levels[weak]}) দিয়ে শুরু করুন — আপনার কোর্সে এই পাঠগুলো আগে রাখা হয়েছে। "
                      f"প্রতিটি পাঠ শেষে self-test দিন।",
        "strengths": [f"{names[strong]}: level {test.levels[strong]}"],
        "focus": [f"{names[weak]}: level {test.levels[weak]}"] + mistakes[:2],
        "tips": [SKILL_TIPS[weak], SKILL_TIPS[order[1]]],
    }
