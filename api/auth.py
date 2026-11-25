"""Who is calling: the family (from the login token) and the learner (from the X-Learner header).

The phone app logs in once with the family's email and password and gets a token. Every later
request sends:
    Authorization: Token <token>
    X-Learner: <learner id>        (which child or adult is learning right now)
"""

from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import BasePermission

from core.models import Learner
from core.utils import get_family


def family_of(request):
    family = get_family(request.user)
    if not family:
        raise PermissionDenied("Create your family on the website first.")
    return family


def learner_of(request):
    family = family_of(request)
    raw = request.headers.get("X-Learner") or request.query_params.get("learner")
    if not raw or not str(raw).isdigit():
        raise NotFound("Choose a learner: send the X-Learner header.")
    learner = Learner.objects.filter(pk=int(raw), family=family).first()
    if not learner:
        raise NotFound("That learner is not in your family.")
    request.family, request.learner = family, learner
    return learner


class HasPaidPlan(BasePermission):
    message = "This part is in the family plan (৳299 a month). Phonics and the first unit are free."

    def has_permission(self, request, view):
        return family_of(request).has_full_access
