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
