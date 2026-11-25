from django import forms
from django.contrib.auth import get_user_model

from core.forms import INPUT, SignupForm

from .data import countries, languages, normalise_phone
from .models import Profile
from .translate import text

User = get_user_model()


def _t(s, lang):
    return text(s, lang)


class GlobalSignupForm(SignupForm):
    """Sign-up for any country: language, country (dial code set automatically), mobile, email, password."""
    language = forms.ChoiceField()
    country = forms.ChoiceField()
    phone = forms.CharField(max_length=20)

    field_order = ["language", "country", "phone", "first_name", "email", "password1", "password2", "family_name", "relation"]

    def __init__(self, *args, lang="en", **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = lang
        self.fields["language"].choices = [(c, f"{native} — {ui}" if native != ui else native) for c, native, ui in languages(lang)]
        self.fields["country"].choices = [(c["iso"], f"{c['flag']} {c['name']} (+{c['dial']})") for c in countries(lang)]
        labels = {
            "language": "Language", "country": "Country", "phone": "Mobile number", "first_name": "Your name",
            "email": "Email", "password1": "Password", "password2": "Password again",
            "family_name": "Family name (optional)", "relation": "You are the (optional)",
        }
        for name, label in labels.items():
            if name in self.fields:
                self.fields[name].label = _t(label, lang)
                self.fields[name].help_text = ""
        self.fields["phone"].widget.attrs.update({"inputmode": "tel", "autocomplete": "tel-national", "class": INPUT})
        self.fields["email"].widget.attrs.update({"autocomplete": "email"})
        for f in ("language", "country"):
            self.fields[f].widget.attrs["class"] = INPUT

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        old = User.objects.filter(username=email).first()
        if old:
            p = Profile.objects.filter(user=old).first()
            if old.is_active or (p and p.email_verified):
                raise forms.ValidationError(_t("An account with this email already exists. Please sign in.", self.lang))
            old.delete()  # an unfinished sign-up that was never confirmed
        return email

    def clean(self):
        data = super().clean()
        iso, raw = data.get("country"), data.get("phone")
        if iso and raw:
            phone = normalise_phone(raw, iso)
            if not phone:
                self.add_error("phone", _t("This mobile number does not look right for the country you chose.", self.lang))
            elif Profile.objects.filter(phone=phone, user__is_active=True).exists():
                self.add_error("phone", _t("This mobile number is already used by another account.", self.lang))
            else:
                data["phone_e164"] = phone
        return data


class CodeForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6, widget=forms.TextInput(attrs={
        "inputmode": "numeric", "autocomplete": "one-time-code", "pattern": "[0-9]{6}", "class": INPUT + " otp-input",
        "placeholder": "••••••"}))


class CodeLoginForm(forms.Form):
    """Sign in with a code: email, or country + mobile number."""
    who = forms.CharField(max_length=200)
    country = forms.ChoiceField(required=False)

    def __init__(self, *args, lang="en", **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = lang
        self.fields["who"].label = _t("Email or mobile number", lang)
        self.fields["who"].widget.attrs.update({"class": INPUT, "autocomplete": "username"})
        self.fields["country"].label = _t("Country (for a mobile number)", lang)
        self.fields["country"].choices = [(c["iso"], f"{c['flag']} {c['name']} (+{c['dial']})") for c in countries(lang)]
        self.fields["country"].widget.attrs["class"] = INPUT

    def user(self):
        who = self.cleaned_data["who"].strip()
        if "@" in who:
            from django.db.models import Q
            return User.objects.filter(Q(username=who.lower()) | Q(email__iexact=who)).order_by("-is_active", "pk").first()
        phone = normalise_phone(who, self.cleaned_data.get("country") or "BD")
        p = Profile.objects.filter(phone=phone).select_related("user").first() if phone else None
        return p.user if p else None
