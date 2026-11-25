from django.contrib import admin

from .models import Attempt, Bookmark, Certificate, LessonDone, Wallet


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("learner", "kind", "key", "item", "score", "created_at")
    list_filter = ("kind",)
    search_fields = ("learner__name", "key", "item")


@admin.register(LessonDone)
class LessonDoneAdmin(admin.ModelAdmin):
    list_display = ("learner", "key", "title", "score", "finished_at")
    search_fields = ("learner__name", "key")


admin.site.register(Bookmark)
admin.site.register(Wallet)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("number", "learner", "title", "issued_at")
