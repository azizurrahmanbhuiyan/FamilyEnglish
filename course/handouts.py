"""The FamilyEnglish Pronunciation Handbook: 23 printable PDF lessons.

The files live in course/handouts/ (not in static/), so they are served only through
course.views.handout, which checks the family plan. Lessons 01 and 02 are free for everyone.
"""

from pathlib import Path

DIR = Path(__file__).resolve().parent / "handouts"
FREE = {1, 2}

# number: (title, title_bn, course lessons that link to it)
HANDOUTS = {
    1: ("Pronunciation basics", "উচ্চারণের ভিত্তি", ["pr-h01"]),
    2: ("Phonemic chart", "ধ্বনির চার্ট", ["pr-h02"]),
    3: ("All British vowel sounds", "ব্রিটিশ ইংরেজির সব স্বরধ্বনি", ["pr-e2"]),
    4: ("Long EE vs short I", "লম্বা EE বনাম ছোট I", ["pr-e3"]),
    5: ("A vs E sounds", "A বনাম E ধ্বনি", ["pr-e2"]),
    6: ("The schwa sound", "শোয়া ধ্বনি /ə/", ["pr-m2"]),
    7: ("Triphthongs", "ত্রিস্বর", ["pr-h07"]),
    8: ("TH sound vs D sound", "TH বনাম D ধ্বনি", ["pr-h08"]),
    9: ("Voiced and voiceless final consonants", "শেষের কণ্ঠস্বরযুক্ত ও কণ্ঠস্বরহীন ব্যঞ্জন", ["pr-e10"]),
    10: ("The R sound", "R ধ্বনি", ["pr-e1", "pr-a2"]),
    11: ("-ED endings", "-ED-এর উচ্চারণ", ["pr-m1"]),
    12: ("Suffixes", "প্রত্যয়", ["pr-h12"]),
    13: ("Silent letters", "নীরব অক্ষর", ["pr-h13"]),
    14: ("30 commonly mispronounced words", "৩০টি প্রায়ই ভুল উচ্চারিত শব্দ", ["pr-h14"]),
    15: ("Weak forms", "দুর্বল রূপ", ["pr-m9"]),
    16: ("Reductions and contractions", "সংক্ষিপ্ত রূপ", ["pr-a7", "pr-a8", "pr-a9"]),
    17: ("Intonation", "সুর (ইনটোনেশন)", ["pr-a5", "pr-a6"]),
    18: ("British accent: RP and Modern RP", "ব্রিটিশ উচ্চারণ: RP ও Modern RP", ["pr-h18"]),
    19: ("Story practice: beginner to advanced", "গল্পে অনুশীলন: শুরু থেকে উচ্চ স্তর", ["pr-h19"]),
    20: ("Story practice: phonetic transcription", "গল্পে অনুশীলন: ধ্বনিলিপি", ["pr-h20"]),
    21: ("Story practice: connected speech", "গল্পে অনুশীলন: জোড়া কথা", ["pr-h21"]),
    22: ("Extra: all English tenses A1–B2", "অতিরিক্ত: সব কাল A1–B2", ["gr-all-tenses"]),
    23: ("Extra: vocabulary and quiz", "অতিরিক্ত: শব্দভান্ডার ও কুইজ", ["rd-family-qa"]),
}


def path(n):
    return DIR / f"FamilyEnglish-Lesson-{n:02d}.pdf"


def items():
    return [{"n": n, "num": f"{n:02d}", "title": t, "title_bn": tb, "free": n in FREE, "lessons": ls}
            for n, (t, tb, ls) in HANDOUTS.items()]


def for_lesson(slug):
    return [i for i in items() if slug in i["lessons"]]
