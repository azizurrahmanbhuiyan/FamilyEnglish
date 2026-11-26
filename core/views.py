from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from learning.models import Level, Progress
from learning.planner import streak

from .forms import (INPUT, FamilyForm, LearnerForm, ManagerForm, PaymentForm, PinForm,
                    SignupForm)
from . import sslcommerz
from .models import PLAN_PRICES_BDT, PLAN_PRICES_USD, Family, FamilyManager, Learner, PaymentRequest, Plan, plan_price
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


def price_context(country):
    """Prices to show: taka in Bangladesh, US dollars elsewhere."""
    if (country or "BD") == "BD":
        return {"prices": PLAN_PRICES_BDT, "sym": "৳", "usd": False}
    per = {k: f"{v / m:.2f}" for k, v, m in ((Plan.HALF_YEAR, PLAN_PRICES_USD[Plan.HALF_YEAR], 6),
                                             (Plan.YEAR, PLAN_PRICES_USD[Plan.YEAR], 12))}
    return {"prices": PLAN_PRICES_USD, "sym": "$", "usd": True, "per_month": per}


def home(request):
    return render(request, "core/home.html", {
        "levels": Level.objects.all(),
        **price_context(_viewer_country(request)),
    })


def _viewer_country(request):
    from .utils import get_family
    fam = get_family(request.user)
    if fam is not None and fam.country:
        return fam.country
    from world.data import guess
    return guess(request)[0]


def pricing(request):
    from django.conf import settings as dj
    iso = _viewer_country(request)
    free_here = bool(dj.FE_FREE_OUTSIDE_BD and iso != "BD")
    return render(request, "core/pricing.html", {**price_context(iso), "free_here": free_here})


def signup(request):
    if request.user.is_authenticated:
        return redirect("core:profiles")
    # Refer & earn: remember an invite code from the link (?ref=FEXXXXXX)
    ref = (request.GET.get("ref") or "").strip().upper()
    if ref:
        request.session["ref_code"] = ref
    inviter = Family.objects.filter(referral_code=request.session.get("ref_code") or "").first()
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        name = form.cleaned_data.get("family_name") or f"{user.first_name}'s family"
        Family.objects.create(name=name, owner=user, referred_by=inviter)
        request.session.pop("ref_code", None)
        login(request, user)
        messages.success(request, "Welcome! Now add the people who will learn — children, "
                                  "parents or grandparents.")
        return redirect("core:learner_add")
    return render(request, "core/signup.html", {"form": form, "inviter": inviter,
                                                "extra_days": settings.REFERRAL_EXTRA_TRIAL_DAYS})


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
                return redirect("studio:today")
            messages.error(request, "That code is not right. Try again.")
        return render(request, "core/pin.html", {"learner": learner, "form": form})
    request.session["learner_id"] = learner.id
    return redirect("studio:today")


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
    if fam.is_free_country:
        from world.middleware import current_lang
        from world.translate import text
        messages.success(request, text("Good news: FamilyEnglish is free in your country for now. Nothing to pay.", current_lang(request)))
        return redirect("core:family")
    initial_plan = request.GET.get("plan", Plan.MONTHLY)
    form = PaymentForm(request.POST or None, initial={"plan": initial_plan})
    if request.method == "POST" and (fam.country or "BD") != "BD":
        return redirect("core:pay")  # bKash/Nagad Send Money is for Bangladesh; others pay online
    if request.method == "POST" and form.is_valid():
        payment = form.save(commit=False)
        payment.family = fam
        payment.paid_by = request.user
        payment.amount_bdt = PLAN_PRICES_BDT[payment.plan]
        payment.save()
        messages.success(request, "Thank you! We will confirm your payment shortly and switch "
                                  "the whole family to the new plan.")
        return redirect("core:family")
    plans = [(p, *plan_price(p, fam.country)) for p in (Plan.MONTHLY, Plan.HALF_YEAR, Plan.YEAR)]
    return render(request, "core/pay.html", {
        "form": form, "family": fam, "prices": PLAN_PRICES_BDT, **price_context(fam.country),
        "plans": [{"code": p, "name": Plan(p).label, "currency": c, "amount": a} for p, c, a in plans],
        "chosen": initial_plan, "online": sslcommerz.enabled(), "in_bd": (fam.country or "BD") == "BD",
        "payments": fam.payments.all()[:5],
    })


@family_required
@require_POST
def pay_online(request):
    """Start an SSLCommerz payment (card, mobile banking, internet banking)."""
    fam = request.family
    plan = request.POST.get("plan")
    if plan not in (Plan.MONTHLY, Plan.HALF_YEAR, Plan.YEAR) or not sslcommerz.enabled():
        return redirect("core:pay")
    currency, amount = plan_price(plan, fam.country)
    p = PaymentRequest.objects.create(
        family=fam, paid_by=request.user, plan=plan, method=PaymentRequest.Method.SSLCOMMERZ,
        transaction_id=sslcommerz.new_tran_id(), currency=currency, amount=amount,
        amount_bdt=amount if currency == "BDT" else 0)
    try:
        return redirect(sslcommerz.start(p, request))
    except sslcommerz.GatewayError as exc:
        p.status, p.note = PaymentRequest.Status.FAILED, str(exc)[:200]
        p.save(update_fields=["status", "note"])
        messages.error(request, str(exc))
        return redirect("core:pay")


# SSLCommerz posts these from its own site, so there is no CSRF token and (with SameSite cookies) often no
# session. Each one validates with SSLCommerz, then sends the browser to a normal page that has the session.

@csrf_exempt
def sslc_success(request):
    d = request.POST or request.GET
    p = sslcommerz.settle(d.get("tran_id"), d.get("val_id"))
    return redirect(reverse("core:pay_result") + "?t=" + (p.transaction_id if p else ""))


@csrf_exempt
def sslc_fail(request):
    sslcommerz.mark((request.POST or request.GET).get("tran_id"), PaymentRequest.Status.FAILED)
    return redirect(reverse("core:pay_result") + "?t=" + (request.POST or request.GET).get("tran_id", ""))


@csrf_exempt
def sslc_cancel(request):
    sslcommerz.mark((request.POST or request.GET).get("tran_id"), PaymentRequest.Status.CANCELLED)
    return redirect(reverse("core:pay_result") + "?t=" + (request.POST or request.GET).get("tran_id", ""))


@csrf_exempt
@require_POST
def sslc_ipn(request):
    """Server-to-server notice from SSLCommerz (also set this URL in the merchant panel → IPN settings)."""
    from django.http import HttpResponse
    d = request.POST
    if d.get("status") in ("VALID", "VALIDATED"):
        sslcommerz.settle(d.get("tran_id"), d.get("val_id"))
    elif d.get("status") in ("FAILED", "CANCELLED", "EXPIRED"):
        sslcommerz.mark(d.get("tran_id"), PaymentRequest.Status.FAILED if d.get("status") != "CANCELLED"
                        else PaymentRequest.Status.CANCELLED)
    return HttpResponse("OK")


@family_required
def pay_result(request):
    p = PaymentRequest.objects.filter(family=request.family, transaction_id=request.GET.get("t", "")).first()
    if p and p.status == PaymentRequest.Status.PENDING and p.method == PaymentRequest.Method.SSLCOMMERZ and p.val_id:
        p = sslcommerz.settle(p.transaction_id, p.val_id) or p  # SSLCommerz was slow before: try again now
        request.family.refresh_from_db()
    return render(request, "core/pay_result.html", {"p": p, "family": request.family})


def switch_learner(request):
    request.session.pop("learner_id", None)
    return redirect("core:profiles")


WORKSHEETS = [
    ("1-letter-sounds", "🔤", "Letter sounds", "অক্ষরের ধ্বনি",
     "Sound chart with pictures, first-sound game, cut-out sound cards, progress chart, sound hunt."),
    ("2-letter-formation", "✏️", "Letter formation", "অক্ষর লেখা",
     "Pencil grip, every letter to trace on handwriting lines, b and d, write your name."),
    ("3-blending-reading", "📖", "Blending and reading", "জুড়ে পড়া",
     "Word lists with sound buttons, digraphs, four-sound words, match words to pictures, sentences."),
    ("4-segmenting-spelling", "🧩", "Hearing sounds and spelling", "ধ্বনি শুনে বানান",
     "Sound boxes, how many sounds, a dictation page with words for parents, draw and write."),
    ("5-tricky-words", "⭐", "Tricky words", "কঠিন শব্দ",
     "24 common tricky words with the tricky part in red, Look-Say-Cover-Write-Check, sentences, word cards."),
]


def worksheets(request):
    """Free printable phonics worksheets — no account needed."""
    from django.templatetags.static import static
    items = [{"slug": s, "icon": i, "title": t, "title_bn": tb, "desc": d,
              "url": static(f"downloads/phonics/familyenglish-phonics-{s}.pdf")} for s, i, t, tb, d in WORKSHEETS]
    return render(request, "core/worksheets.html", {"items": items})


def privacy(request):
    return render(request, "core/privacy.html")



def password(request):
    """Change the password (old one needed), or set a new one after a 'Forgot password?' code."""
    from django.contrib.auth import update_session_auth_hash
    from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm

    from .forms import INPUT

    if not request.user.is_authenticated:
        return redirect("core:login")
    user = request.user
    reset = bool(request.session.get("may_set_password")) or not user.has_usable_password()
    Form = SetPasswordForm if reset else PasswordChangeForm
    form = Form(user, request.POST or None)
    for f in form.fields.values():
        f.widget.attrs.setdefault("class", INPUT)
    if request.method == "POST" and form.is_valid():
        form.save()
        update_session_auth_hash(request, user)
        request.session.pop("may_set_password", None)
        messages.success(request, "Your new password is saved. Use it on the website and in the app. / "
                                  "নতুন পাসওয়ার্ড সেভ হয়েছে। ওয়েবসাইট ও অ্যাপে এটি ব্যবহার করুন।")
        return redirect("core:profiles")
    return render(request, "core/password.html", {"form": form, "reset": reset})
