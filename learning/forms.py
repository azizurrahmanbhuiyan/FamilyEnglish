from django import forms

from core.forms import INPUT

LEVEL_CHOICES = [(i, f"Level {i}") for i in range(9)]


class PlanForm(forms.Form):
    start_level = forms.TypedChoiceField(choices=LEVEL_CHOICES, coerce=int, label="Start at")
    finish_level = forms.TypedChoiceField(choices=LEVEL_CHOICES, coerce=int, label="Finish level")
    months = forms.TypedChoiceField(choices=[(m, f"{m} month{'s' if m > 1 else ''}") for m in range(1, 13)],
                                    coerce=int, label="Time you have")
    days_per_week = forms.TypedChoiceField(choices=[(3, "3 days"), (4, "4 days"), (5, "5 days (Sun–Thu)"),
                                                    (6, "6 days (Sat–Thu)")],
                                           coerce=int, label="Study days a week")
    minutes_per_day = forms.TypedChoiceField(choices=[(15, "15 min"), (20, "20 min"), (30, "30 min")],
                                             coerce=int, label="Minutes a day")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs["class"] = INPUT

    def clean(self):
        data = super().clean()
        if data.get("finish_level") is not None and data.get("start_level") is not None:
            if data["finish_level"] < data["start_level"]:
                raise forms.ValidationError("The finish level must be the same as or higher than the start.")
        return data
