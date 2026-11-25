from django.contrib import admin

from learning.admin import VideoClipInline

from .models import AnswerLog, CourseLesson, CourseProgress, SelfTestAttempt, SmartTest


@admin.register(CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    list_display = ("title", "skill", "band", "order")
    list_filter = ("skill", "band")
    search_fields = ("title", "title_bn", "slug")
    inlines = [VideoClipInline]


@admin.register(SmartTest)
class SmartTestAdmin(admin.ModelAdmin):
    list_display = ("learner", "started_at", "finished_at", "levels", "ai_used")
    readonly_fields = ("answers", "scores", "levels", "bands", "report")


@admin.register(SelfTestAttempt)
class SelfTestAttemptAdmin(admin.ModelAdmin):
    list_display = ("learner", "lesson", "score", "total", "passed", "created_at")
    list_filter = ("passed",)


admin.site.register(CourseProgress)
admin.site.register(AnswerLog)
