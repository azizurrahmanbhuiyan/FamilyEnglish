from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

from .models import Learner, PaymentRequest, Plan

User = get_user_model()

INPUT = "w-full rounded-xl border border-stone-300 px-3 py-2 focus:border-rose-500 focus:ring-rose-500"


class StyledMixin:
    def _style(self):
        for f in self.fields.values():
            if isinstance(f.widget, (forms.CheckboxInput, forms.RadioSelect)):
                continue
            f.widget.attrs.setdefault("class", INPUT)


class SignupForm(StyledMixin, UserCreationForm):
    first_name = forms.CharField(label="Your name", max_length=60)
    email = forms.EmailField(label="Email (used to sign in)")
    family_name = forms.CharField(label="Family name", max_length=120,
                                  help_text="e.g. Bhuiyan family", required=False)
    relation = forms.CharField(label="You are the", max_length=40, required=False,
                               help_text="Father, mother, grandmother, uncle …")

    class Meta:
        model = User
        fields = ("first_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("An account with this email already exists. Please sign in.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        if commit:
            user.save()
        return user


class FamilyForm(StyledMixin, forms.Form):
    family_name = forms.CharField(max_length=120)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()


class LearnerForm(StyledMixin, forms.ModelForm):
    pin = forms.CharField(label="4-digit code (optional)", required=False, max_length=4, min_length=4,
                          widget=forms.PasswordInput(render_value=False, attrs={"inputmode": "numeric"}),
                          help_text="Lets a child open only their own profile. Leave blank for none.")
    avatar = forms.ChoiceField(choices=[(a, a) for a in Learner.AVATARS], widget=forms.RadioSelect)

    class Meta:
        model = Learner
        fields = ("name", "role", "birth_year", "avatar", "daily_limit_minutes")
        labels = {"birth_year": "Birth year", "daily_limit_minutes": "Daily screen limit (minutes)"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    def clean_birth_year(self):
        year = self.cleaned_data.get("birth_year")
        this_year = timezone.localdate().year
        if year and not (this_year - 100 <= year <= this_year - 2):
            raise forms.ValidationError("Please enter a real birth year.")
        return year

    def clean_pin(self):
        pin = self.cleaned_data.get("pin", "")
        if pin and not pin.isdigit():
            raise forms.ValidationError("Use 4 digits.")
        return pin

    def save(self, commit=True):
        learner = super().save(commit=False)
        if self.cleaned_data.get("pin"):
            learner.set_pin(self.cleaned_data["pin"])
        if commit:
            learner.save()
        return learner


class PinForm(forms.Form):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput(attrs={
        "class": INPUT + " text-center text-3xl tracking-[1em]", "inputmode": "numeric", "autofocus": True}))


class ManagerForm(StyledMixin, forms.Form):
    email = forms.EmailField(help_text="They must sign up first with this email.")
    relation = forms.CharField(max_length=40, required=False, help_text="e.g. Mother, Grandfather")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        try:
            self.user = User.objects.get(username=email)
        except User.DoesNotExist:
            raise forms.ValidationError("No FamilyEnglish account uses this email yet. Ask them to sign up first.")
        return email


class PaymentForm(StyledMixin, forms.ModelForm):
    plan = forms.ChoiceField(choices=[c for c in Plan.choices if c[0] != Plan.FREE])

    class Meta:
        model = PaymentRequest
        fields = ("plan", "method", "transaction_id")
        labels = {"transaction_id": "Transaction ID (TrxID)"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["method"].choices = [(PaymentRequest.Method.BKASH, "bKash"), (PaymentRequest.Method.NAGAD, "Nagad")]
        self._style()


def max_learners():
    return settings.FAMILY_MAX_LEARNERS
