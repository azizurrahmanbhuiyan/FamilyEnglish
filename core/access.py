"""Who can open what.

Free for every family, forever: the first two weeks of the Phonics Year (10 lessons: the sounds
s a t i p n and c/k e h r m d), the printable phonics worksheets and the sound pages. The other 34
weeks are in the family plan. Everything else needs a paid family plan (৳299 a month, ৳1500 for 6 months or
৳2500 for a year), which covers every learner in the family.
"""

from functools import wraps

from django.shortcuts import render

from .utils import family_required, learner_required

FREE_SKILLS = {"phonics"}
FREE_PHONICS_WEEKS = 2  # weeks 1-2 of the Phonics Year


def is_free_lesson(lesson):
    if lesson.skill not in FREE_SKILLS:
        return False
    week = (lesson.module.plan or {}).get("week")
    return week is not None and week <= FREE_PHONICS_WEEKS


def can_open_lesson(family, lesson):
    return family.has_full_access or is_free_lesson(lesson)


def locked(request, feature_en="", feature_bn=""):
    """The friendly 'this part is in the family plan' page (status 402 so tests and logs can tell)."""
    from .models import PLAN_PRICES_BDT
    return render(request, "core/locked.html", {
        "feature_en": feature_en, "feature_bn": feature_bn, "prices": PLAN_PRICES_BDT,
    }, status=402)


def paid_required(feature_en="", feature_bn="", free_if=None, learner=True):
    """Decorator: the view needs a paid plan, unless free_if(request, *args, **kwargs) says it is free."""
    def deco(view):
        @wraps(view)
        def inner(request, *args, **kwargs):
            if not request.family.has_full_access and not (free_if and free_if(request, *args, **kwargs)):
                return locked(request, feature_en, feature_bn)
            return view(request, *args, **kwargs)
        return (learner_required if learner else family_required)(inner)
    return deco
