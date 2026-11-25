from django.contrib import admin

from .models import FeatureIdea, LearnerGoal, XPEvent


@admin.register(FeatureIdea)
class FeatureIdeaAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "created_at")
    list_filter = ("status",)
    list_editable = ("status",)


@admin.register(XPEvent)
class XPEventAdmin(admin.ModelAdmin):
    list_display = ("learner", "amount", "reason", "created_at")


admin.site.register(LearnerGoal)
