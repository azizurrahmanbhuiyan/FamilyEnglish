"""Optional AI (Anthropic Messages API) with safe, child-friendly defaults.

Set FE_AI_API_KEY in .env to switch it on. Without a key, or if the call fails,
callers fall back to FamilyEnglish's built-in rule-based answers, so every page
still works. Uses only the standard library (no extra package to install).
"""

import json
import logging
import urllib.error
import urllib.request

from django.conf import settings
from django.utils import timezone

log = logging.getLogger(__name__)

API_URL = "https://api.anthropic.com/v1/messages"

SAFETY = (
    "You are talking with a learner on FamilyEnglish, a Bangladeshi family English-learning website. "
    "The learner may be a young child or a parent. Be warm, short and encouraging. "
    "Use simple English and add a short Bangla explanation when it helps. "
    "Only help with learning English. Politely decline anything else, and never ask for or "
    "repeat personal details such as full names, addresses, phone numbers or schools. "
    "If a child seems upset or unsafe, kindly tell them to talk to a parent or a trusted adult."
)


def enabled():
    return bool(settings.AI_API_KEY)


def used_today(learner):
    """AI replies this learner received today (tutor + writing helper + speaking feedback)."""
    from course.models import AnswerLog
    from learning.models import FamilyTalkSet

    from .models import SpeakingAttempt, TutorMessage, WritingAttempt

    start = timezone.localtime().replace(hour=0, minute=0, second=0, microsecond=0)
    return (TutorMessage.objects.filter(learner=learner, role="assistant", ai_used=True,
                                        created_at__gte=start).count()
            + WritingAttempt.objects.filter(learner=learner, ai_used=True, created_at__gte=start).count()
            + SpeakingAttempt.objects.filter(learner=learner, ai_used=True, created_at__gte=start).count()
            + AnswerLog.objects.filter(learner=learner, ai_used=True, created_at__gte=start).count()
            + FamilyTalkSet.objects.filter(learner=learner, created_at__gte=start).count()
            + _studio_used(learner, start))


def _studio_used(learner, start):
    try:
        from studio.models import Attempt
    except ImportError:  # pragma: no cover
        return 0
    return Attempt.objects.filter(learner=learner, ai_used=True, created_at__gte=start).count()


def left_today(learner):
    return max(0, settings.AI_DAILY_LIMIT - used_today(learner))


def ask(system, messages, max_tokens=500, model=None):
    """Return the model's text, or None if AI is off, over the limit or the call failed.

    messages: [{"role": "user"|"assistant", "content": "..."}]
    """
    if not enabled():
        return None
    body = json.dumps({
        "model": model or settings.AI_MODEL,
        "max_tokens": max_tokens,
        "system": SAFETY + "\n\n" + system,
        "messages": messages,
    }).encode()
    req = urllib.request.Request(API_URL, data=body, method="POST", headers={
        "content-type": "application/json",
        "x-api-key": settings.AI_API_KEY,
        "anthropic-version": "2023-06-01",
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
        parts = [b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"]
        text = "".join(parts).strip()
        return text or None
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:  # pragma: no cover
        log.warning("AI call failed: %s", exc)
        return None
