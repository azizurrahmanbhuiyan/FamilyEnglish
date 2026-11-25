from django.contrib import admin

from .models import (Lesson, LessonVideo, Level, Module, Placement, PlacementQuestion, PlanDay,
                     PracticeItem, Progress, StudyPlan)


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "matches", "planned_lessons")
    inlines = [ModuleInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ("order", "title", "skill", "activity", "minutes")


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("__str__", "level", "order")
    list_filter = ("level",)
    inlines = [LessonInline]


class VideoInline(admin.TabularInline):
    model = LessonVideo
    extra = 1
    fields = ("order", "title", "channel", "youtube_id", "search_query", "why_watch_bn", "minutes",
              "made_for_kids")


class ItemInline(admin.TabularInline):
    model = PracticeItem
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "skill", "activity", "video_ids_set")
    list_filter = ("module__level", "skill", "activity")
    search_fields = ("title", "focus")
    inlines = [VideoInline, ItemInline]

    @admin.display(description="Videos with ID", boolean=False)
    def video_ids_set(self, obj):
        total = obj.videos.count()
        with_id = obj.videos.exclude(youtube_id="").count()
        return f"{with_id}/{total}"


@admin.register(LessonVideo)
class LessonVideoAdmin(admin.ModelAdmin):
    list_display = ("title", "channel", "youtube_id", "lesson", "made_for_kids")
    list_filter = ("channel", "made_for_kids")
    search_fields = ("title", "youtube_id", "lesson__title")
    list_editable = ("youtube_id",)


@admin.register(PlacementQuestion)
class PlacementQuestionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "skill", "level", "answer")
    list_filter = ("skill", "level")


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ("learner", "taken_at", "listening", "speaking", "reading", "writing", "overall")


class PlanDayInline(admin.TabularInline):
    model = PlanDay
    extra = 0


@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ("learner", "start_level", "target_level", "start_date", "end_date", "is_active")
    inlines = [PlanDayInline]


admin.site.register(Progress)



# ------------------------------------------------------------------ short video clips
from django import forms as _forms

from .clips import fmt_time, parse_time
from .models import TalkTopic, VideoClip


class VideoClipForm(_forms.ModelForm):
    """Times can be typed as 1:23 or seconds; any YouTube link can be pasted."""

    start = _forms.CharField(help_text="Start, e.g. 1:23", initial="0:00")
    end = _forms.CharField(help_text="End, e.g. 4:10 (max 5 minutes after the start)")

    class Meta:
        model = VideoClip
        fields = ["order", "youtube_id", "start", "end", "title", "channel", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial["start"] = fmt_time(self.instance.start)
            self.initial["end"] = fmt_time(self.instance.end)

    def clean_start(self):
        return parse_time(self.cleaned_data["start"])

    def clean_end(self):
        return parse_time(self.cleaned_data["end"])


class VideoClipInline(admin.TabularInline):
    model = VideoClip
    form = VideoClipForm
    extra = 1
    fields = ["order", "youtube_id", "start", "end", "title", "channel", "status"]


@admin.register(VideoClip)
class VideoClipAdmin(admin.ModelAdmin):
    form = VideoClipForm
    list_display = ["title", "channel", "for_lesson", "times", "status", "source", "say_line"]
    list_filter = ["status", "source"]
    list_editable = ["status"]
    search_fields = ["title", "channel", "youtube_id"]
    fields = ["lesson", "course_lesson", "topic", "order", "youtube_id", "start", "end", "title", "channel", "status",
              "say_line", "say_line_bn", "preview"]
    readonly_fields = ["preview"]
    raw_id_fields = ["lesson", "course_lesson", "topic"]

    class Form(VideoClipForm):
        class Meta(VideoClipForm.Meta):
            fields = ["lesson", "course_lesson", "topic"] + VideoClipForm.Meta.fields + ["say_line", "say_line_bn"]

    def get_form(self, request, obj=None, **kwargs):
        kwargs["form"] = self.Form
        return super().get_form(request, obj, **kwargs)

    @admin.display(description="Lesson")
    def for_lesson(self, obj):
        return obj.lesson or obj.course_lesson or obj.topic

    @admin.display(description="Part")
    def times(self, obj):
        return f"{obj.start_label}–{obj.end_label} ({obj.length_label})"

    @admin.display(description="Preview")
    def preview(self, obj):
        from django.utils.html import format_html
        if not obj.pk:
            return "Save first to preview."
        return format_html('<iframe width="420" height="236" src="{}" allowfullscreen></iframe>', obj.embed_url)


@admin.register(TalkTopic)
class TalkTopicAdmin(admin.ModelAdmin):
    list_display = ["title", "group", "order"]
    list_filter = ["group"]
    inlines = [VideoClipInline]


LessonAdmin.inlines = [VideoClipInline] + list(LessonAdmin.inlines)
