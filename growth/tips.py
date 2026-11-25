"""One short tip a day, aimed at the learner's weakest question type (AI when on, else built-in)."""

from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

QTYPE_TIPS = {
    "listening": "শোনার সময় প্রশ্নের key word আগে পড়ে নিন, তারপর শুধু সেই তথ্যটি খুঁজুন।",
    "speaking": "প্রতিদিন একটি বাক্য রেকর্ড করে নিজে শুনুন — উচ্চারণ ধীরে ধীরে পরিষ্কার হবে।",
    "reading": "প্রতিটি অনুচ্ছেদের প্রথম বাক্য আগে পড়ুন — মূল ভাবনা দ্রুত ধরা যায়।",
    "writing": "লেখা শেষে ১ মিনিট সময় নিয়ে বড় হাতের অক্ষর, দাঁড়ি আর verb-এর -s দেখে নিন।",
    "grammar": "আজকের ভুলটি খাতায় লিখুন: ভুল → সঠিক → কারণ। কাল আবার পড়ুন।",
}


def daily_tip(request, learner):
    from course.models import AnswerLog
    from course.qtypes import QTYPES, label
    from practice import ai

    key = f"tip-{learner.id}-{timezone.localdate().isoformat()}"
    if key in request.session:
        return request.session[key]
    since = timezone.now() - timedelta(days=30)
    weak = (AnswerLog.objects.filter(learner=learner, correct=False, created_at__gte=since).exclude(qtype="")
            .values("qtype").annotate(n=Count("id")).order_by("-n").first())
    focus = label(weak["qtype"]) if weak else None
    skill = QTYPES.get(weak["qtype"], ("grammar",))[0] if weak else None
    text, used_ai = None, False
    if focus and ai.enabled() and ai.left_today(learner) > 0:
        text = ai.ask("Give ONE practical English study tip (max 2 short sentences in Bangla, English examples "
                      "allowed) for a learner whose weakest area is the one given. No greeting.",
                      [{"role": "user", "content": f"Weakest area: {focus}"}], max_tokens=150)
        used_ai = bool(text)
    if not text:
        text = QTYPE_TIPS.get(skill) if skill else \
            "আজ ১০ মিনিট সময় দিন: একটি পাঠ, একটি সেলফ-টেস্ট, আর পরিবারের সাথে একটি ইংরেজি বাক্য।"
    tip = {"focus": focus, "text": text.strip()[:400], "ai": used_ai}
    request.session[key] = tip
    return tip
