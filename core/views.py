from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from learning.models import Level, Progress
from learning.planner import streak

from .forms import (INPUT, FamilyForm, LearnerForm, ManagerForm, PaymentForm, PinForm,
                    SignupForm)
from .models import PLAN_PRICES_BDT, Family, FamilyManager, Learner, Plan
from .utils import family_required, get_family


class EmailAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"
        for f in self.fields.values():
            f.widget.attrs["class"] = INPUT

    def clean(self):
        if self.data.get("username"):
            self.data = self.data.copy()
            self.data["username"] = self.data["username"].lower().strip()
        return super().clean()


class FamilyLoginView(LoginView):
    template_name = "core/login.html"
    authentication_form = EmailAuthForm


def home(request):
    return render(request, "core/home.html", {
        "levels": Level.objects.all(),
        "prices": PLAN_PRICES_BDT,
    })


def pricing(request):
    return render(request, "core/pricing.html", {"prices": PLAN_PRICES_BDT})


def signup(request):
    if request.user.is_authenticated:
        return redirect("core:profiles")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        name = form.cleaned_data.get("family_name") or f"{user.first_name}'s family"
        Family.objects.create(name=name, owner=user)
        login(request, user)
        messages.success(request, "Welcome! Now add the people who will learn — children, "
                                  "parents or grandparents.")
        return redirect("core:learner_add")
    return render(request, "core/signup.html", {"form": form})


@login_required
def family_create(request):
    if get_family(request.user):
        return redirect("core:profiles")
    form = FamilyForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        Family.objects.create(name=form.cleaned_data["family_name"], owner=request.user)
        return redirect("core:learner_add")
    return render(request, "core/family_create.html", {"form": form})


@family_required
def profiles(request):
    learners = request.family.learners.all()
    if not learners:
        return redirect("core:learner_add")
    return render(request, "core/profiles.html", {"learners": learners})


@family_required
def choose_learner(request, pk):
    learner = get_object_or_404(Learner, pk=pk, family=request.family)
    if learner.pin_hash:
        form = PinForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            if learner.check_pin(form.cleaned_data["pin"]):
                request.session["learner_id"] = learner.id
                return redirect("learning:today")
            messages.error(request, "That code is not right. Try again.")
        return render(request, "core/pin.html", {"learner": learner, "form": form})
    request.session["learner_id"] = learner.id
    return redirect("learning:today")


@family_required
def learner_add(request):
    if request.family.learners.count() >= settings.FAMILY_MAX_LEARNERS:
        messages.warning(request, f"A family can have up to {settings.FAMILY_MAX_LEARNERS} learners.")
        return redirect("core:profiles")
    form = LearnerForm(request.POST or None, initial={"avatar": Learner.AVATARS[0]})
    if request.method == "POST" and form.is_valid():
        learner = form.save(commit=False)
        learner.family = request.family
        learner.save()
        messages.success(request, f"{learner.name} is ready. Next: a short placement test.")
        request.session["learner_id"] = learner.id
        return redirect("learning:placement_start")
    return render(request, "core/learner_form.html", {"form": form, "adding": True})


@family_required
def learner_edit(request, pk):
    learner = get_object_or_404(Learner, pk=pk, family=request.family)
    form = LearnerForm(request.POST or None, instance=learner)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile saved.")
        return redirect("core:family")
    return render(request, "core/learner_form.html", {"form": form, "learner": learner})


@require_POST
@family_required
def learner_delete(request, pk):
    learner = get_object_or_404(Learner, pk=pk, family=request.family)
    if request.session.get("learner_id") == learner.id:
        request.session.pop("learner_id")
    learner.delete()
    messages.success(request, "Profile and its progress deleted.")
    return redirect("core:family")


@family_required
def family(request):
    """Parent dashboard: every learner's levels, plan progress and streak."""
    fam = request.family
    rows = []
    for learner in fam.learners.all():
        placement = learner.placements.first()
        plan = learner.plans.filter(is_active=True).first()
        done, total = plan.progress() if plan else (0, 0)
        rows.append({
            "learner": learner,
            "placement": placement,
            "plan": plan,
            "done": done,
            "total": total,
            "percent": round(done * 100 / total) if total else 0,
            "streak": streak(learner),
            "recent": Progress.objects.filter(learner=learner).select_related("lesson")[:3],
        })
    return render(request, "core/family.html", {
        "family": fam,
        "rows": rows,
        "managers": fam.memberships.select_related("user"),
        "manager_form": ManagerForm(),
        "is_owner": fam.owner_id == request.user.id,
        "can_add": fam.learners.count() < settings.FAMILY_MAX_LEARNERS,
    })


@require_POST
@family_required
def manager_add(request):
    fam = request.family
    if fam.owner_id != request.user.id:
        messages.error(request, "Only the account owner can add co-managers.")
        return redirect("core:family")
    form = ManagerForm(request.POST)
    if form.is_valid():
        if form.user.id == fam.owner_id:
            messages.info(request, "You already own this family account.")
        elif get_family(form.user) and get_family(form.user) != fam:
            messages.error(request, "That person already belongs to another family account.")
        else:
            FamilyManager.objects.get_or_create(family=fam, user=form.user,
                                                defaults={"relation": form.cleaned_data["relation"]})
            messages.success(request, f"{form.user.first_name or form.user.email} can now manage this family.")
    else:
        messages.error(request, " ".join(form.errors.get("email", ["Check the email."])))
    return redirect("core:family")


@require_POST
@family_required
def manager_remove(request, pk):
    fam = request.family
    if fam.owner_id == request.user.id:
        FamilyManager.objects.filter(family=fam, pk=pk).delete()
        messages.success(request, "Co-manager removed.")
    return redirect("core:family")


@family_required
def pay(request):
    """Any adult in the family can pay for the whole family (manual bKash/Nagad for now)."""
    fam = request.family
    initial_plan = request.GET.get("plan", Plan.MONTHLY)
    form = PaymentForm(request.POST or None, initial={"plan": initial_plan})
    if request.method == "POST" and form.is_valid():
        payment = form.save(commit=False)
        payment.family = fam
        payment.paid_by = request.user
        payment.amount_bdt = PLAN_PRICES_BDT[payment.plan]
        payment.save()
        messages.success(request, "Thank you! We will confirm your payment shortly and switch "
                                  "the whole family to the new plan.")
        return redirect("core:family")
    return render(request, "core/pay.html", {
        "form": form, "family": fam, "prices": PLAN_PRICES_BDT,
        "payments": fam.payments.all()[:5],
    })


def switch_learner(request):
    request.session.pop("learner_id", None)
    return redirect("core:profiles")


def privacy(request):
    return render(request, "core/privacy.html")

