"""Built-in feedback that needs no AI: a writing checker, a speaking scorer and tutor FAQ.

The writing checks target mistakes Bangla speakers often make in English.
"""

import re
from difflib import SequenceMatcher

# (pattern, replacement, Bangla explanation). Applied in order, case-insensitive.
COMMON_FIXES = [
    (r"\bcousin (brother|sister)\b", "cousin",
     "ইংরেজিতে 'cousin' একাই যথেষ্ট — 'cousin brother/sister' বলা হয় না।"),
    (r"\bdiscuss about\b", "discuss", "'discuss' এর পরে 'about' লাগে না।"),
    (r"\breturn back\b", "return", "'return' মানেই ফিরে আসা — 'back' বাড়তি।"),
    (r"\bmore better\b", "better", "'better' নিজেই তুলনা — 'more' লাগে না।"),
    (r"\bmore easier\b", "easier", "'easier' নিজেই তুলনা — 'more' লাগে না।"),
    (r"\bI am agree\b", "I agree", "'agree' একটি verb — 'am' লাগে না।"),
    (r"\bI am understand\b", "I understand", "'understand' একটি verb — 'am' লাগে না।"),
    (r"\bvery much like\b", "really like", "স্বাভাবিক ইংরেজি: 'I really like …' বা 'I like … very much'।"),
    (r"\bgive (a )?exam\b", "take an exam", "ইংরেজিতে পরীক্ষা 'give' নয়, 'take' (বা 'sit') করা হয়।"),
    (r"\bhe have\b", "he has", "he/she/it এর সাথে 'have' নয়, 'has'।"),
    (r"\bshe have\b", "she has", "he/she/it এর সাথে 'have' নয়, 'has'।"),
    (r"\bit have\b", "it has", "he/she/it এর সাথে 'have' নয়, 'has'।"),
    (r"\b(he|she|it) (don't)\b", r"\1 doesn't", "he/she/it এর সাথে 'don't' নয়, 'doesn't'।"),
    (r"\b(I|we|you|they|he|she) did (\w+ed)\b", r"\1 \2",
     "হ্যাঁ-বোধক বাক্যে 'did' লাগে না: 'I played', 'did played' নয়।"),
    (r"\btv\b", "TV", "TV সবসময় বড় হাতের অক্ষরে।"),
]

THIRD_PERSON = ["go", "do", "play", "like", "want", "eat", "read", "watch", "live", "work",
                "come", "love", "need", "know", "study", "help", "speak", "write", "teach"]
ES_VERBS = {"go": "goes", "do": "does", "watch": "watches", "teach": "teaches", "study": "studies"}

AN_WORDS = ["apple", "egg", "orange", "umbrella", "elephant", "ice", "hour", "honest", "idea",
            "insect", "ant", "owl", "uncle", "aunt", "island", "onion", "ink", "old"]


def check_writing(text):
    """Return (corrected_text, [Bangla notes]). Simple, predictable rules — not a full grammar check."""
    notes = []
    fixed = text.strip()
    if not fixed:
        return "", []

    for pattern, repl, note in COMMON_FIXES:
        new = re.sub(pattern, repl, fixed, flags=re.IGNORECASE)
        if new != fixed:
            fixed = new
            notes.append(note)

    def third(m):
        subj, verb = m.group(1), m.group(2)
        lower = verb.lower()
        return f"{subj} {ES_VERBS.get(lower, lower + 's')}"

    pattern = r"\b(He|She|It|he|she|it|[Mm]y (?:mother|father|brother|sister|cousin|friend|teacher|uncle|aunt|grandmother|grandfather))\s+(" + "|".join(THIRD_PERSON) + r")\b"
    new = re.sub(pattern, third, fixed)
    if new != fixed:
        fixed = new
        notes.append("he / she / it (বা একজন মানুষ) হলে present simple-এ verb-এর শেষে -s/-es বসে: "
                     "She goes, He plays।")

    new = re.sub(r"\ba (" + "|".join(AN_WORDS) + r")\b", r"an \1", fixed, flags=re.IGNORECASE)
    if new != fixed:
        fixed = new
        notes.append("vowel sound (a, e, i, o, u) দিয়ে শুরু হলে 'a' নয়, 'an': an apple, an egg।")

    new = re.sub(r"(^|[\s.!?])i(?=[\s'.,!?]|$)", lambda m: m.group(1) + "I", fixed)
    if new != fixed:
        fixed = new
        notes.append("'I' (আমি) সবসময় বড় হাতের অক্ষরে লেখা হয়।")

    sentences = re.split(r"(?<=[.!?])\s+", fixed)
    capped = [s[:1].upper() + s[1:] if s else s for s in sentences]
    new = " ".join(capped)
    if new != fixed:
        fixed = new
        notes.append("প্রতিটি বাক্য বড় হাতের অক্ষর (capital letter) দিয়ে শুরু হয়।")

    new = re.sub(r"\s+([,.!?])", r"\1", fixed)
    new = re.sub(r"([,.!?])(?=[A-Za-z])", r"\1 ", new)
    new = re.sub(r" {2,}", " ", new)
    if new != fixed:
        fixed = new
        notes.append("কমা/দাঁড়ির আগে space নয়, পরে একটা space।")

    if fixed and fixed[-1] not in ".!?":
        fixed += "."
        notes.append("বাক্যের শেষে full stop (.) বা প্রশ্নবোধক চিহ্ন (?) দিন।")

    return fixed, notes


def _words(text):
    return re.findall(r"[a-z']+", (text or "").lower())


def speaking_score(target, heard):
    """0-100: how much of the target sentence was heard, in order."""
    t, h = _words(target), _words(heard)
    if not t or not h:
        return 0
    return round(SequenceMatcher(None, t, h).ratio() * 100)


def missed_words(target, heard):
    heard_set = set(_words(heard))
    return [w for w in _words(target) if w not in heard_set]


# ------------------------------------------------------------------ tutor FAQ (no AI)

FAQ = [
    (("letter name", "sound", "phonics", "ফনিক্স"),
     "Teach the **sound**, not the letter name: s says “sss”, not “es”. "
     "বাংলায়: অক্ষরের নাম নয়, শব্দটা (sound) শেখান। Level 0 lessons show one sound each day."),
    (("plan", "month", "পরিকল্পনা", "প্ল্যান", "রুটিন"),
     "Go to **Study plan → Change the plan**. Pick a finish level and the months you have; "
     "finished lessons are kept. বাংলায়: মাস আর লেভেল বেছে নিলে প্রতিদিনের পড়া ঠিক হয়ে যায়।"),
    (("pay", "bkash", "nagad", "price", "টাকা", "পেমেন্ট", "বিকাশ", "নগদ"),
     "Phonics is free. One Family plan (৳299 a month, ৳1500 for 6 months, ৳2500 a year) covers up to 6 learners. Any adult can pay with bKash or Nagad on the "
     "**Subscription** page. বাংলায়: পরিবারের যেকোনো বড় সদস্য টাকা দিতে পারেন।"),
    ((" v ", " w ", "very", "water", " vest"),
     "For **v**, top teeth touch the bottom lip (very). For **w**, round your lips, no teeth (water). "
     "বাংলায়: v-তে দাঁত ঠোঁটে লাগে, w-তে ঠোঁট গোল হয়।"),
    (("th", "think", "three", "“th”", "\"th\""),
     "For **th**, put your tongue lightly between your teeth: think, three (just air); this, that (voice on). "
     "বাংলায়: জিভ দুই দাঁতের মাঝে রাখুন — 'ট' বা 'দ' নয়।"),
    (("past", "yesterday", "went", "গতকাল"),
     "To talk about yesterday, use the past: I **played**, we **went**, she **ate**. "
     "বাংলায়: গতকালের কথা বলতে verb-এর past রূপ লাগে।"),
    (("present", "every day", "goes", "routine"),
     "For habits use the present simple: I **go** to school. With he/she/it add -s: She **goes**. "
     "বাংলায়: he/she/it হলে verb-এ -s/-es যোগ হয়।"),
    (("a or an", "a/an", " an ", " an?", "use an", "\"an\"", "“an”", "article"),
     "Use **an** before a vowel sound: an apple, an egg, an hour. Otherwise **a**: a cat, a book."),
    (("streak", "xp", "star"),
     "Finish a lesson each day to grow your 🔥 streak. Each lesson gives XP, and more stars give more XP."),
]

DEFAULT_ANSWER = (
    "I can help with English sounds, words, grammar and how to use FamilyEnglish. "
    "Try asking: “How do I say th?”, “When do I use an?”, or “How do I change my plan?” "
    "বাংলায়: ইংরেজি শব্দ, উচ্চারণ বা ব্যাকরণ নিয়ে প্রশ্ন করুন।"
)


def faq_answer(question):
    """Match whole words, so 'th' does not match 'the' or 'past'."""
    q = f" {question.lower()} "
    words = set(re.findall(r"[a-z']+|[\u0980-\u09ff]+", q))
    for keys, answer in FAQ:
        for k in keys:
            plain = k.strip()
            if (plain.isalpha() and plain.isascii() and plain in words) or \
                    (not (plain.isalpha() and plain.isascii()) and k in q):
                return answer
    return DEFAULT_ANSWER
