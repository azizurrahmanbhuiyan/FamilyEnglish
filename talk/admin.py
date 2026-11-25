from django.contrib import admin

from .models import Article, TalkProfile, TalkSession


@admin.register(TalkProfile)
class TalkProfileAdmin(admin.ModelAdmin):
    list_display = ("learner", "level", "reason", "correct", "daily_minutes", "done")


@admin.register(TalkSession)
class TalkSessionAdmin(admin.ModelAdmin):
    list_display = ("learner", "kind", "title", "created_at", "finished_at")
    list_filter = ("kind",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "slug", "created_at")
    list_filter = ("category",)
    search_fields = ("title", "body")
