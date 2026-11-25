from django.contrib import admin

from .models import (CardReview, SkillCheck, SpeakingAttempt, SupportTicket, TutorMessage, Tutorial,
                     VocabDeck, VocabWord, WritingAttempt)


class WordInline(admin.TabularInline):
    model = VocabWord
    extra = 1


@admin.register(VocabDeck)
class VocabDeckAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "order", "slug")
    list_filter = ("level",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [WordInline]


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "group", "youtube_id")
    list_editable = ("youtube_id",)


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("subject", "family", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("subject", "message", "family__name")
    fields = ("family", "user", "subject", "message", "reply", "status")
    readonly_fields = ("family", "user", "subject", "message")

    def save_model(self, request, obj, form, change):
        if obj.reply and obj.status == SupportTicket.Status.OPEN:
            obj.status = SupportTicket.Status.ANSWERED
        super().save_model(request, obj, form, change)


@admin.register(SkillCheck)
class SkillCheckAdmin(admin.ModelAdmin):
    list_display = ("learner", "kind", "skill", "level", "score", "total", "taken_at")
    list_filter = ("kind", "skill")


@admin.register(TutorMessage)
class TutorMessageAdmin(admin.ModelAdmin):
    list_display = ("learner", "role", "short", "ai_used", "created_at")
    list_filter = ("role", "ai_used")

    @admin.display(description="Message")
    def short(self, obj):
        return obj.text[:80]


admin.site.register(SpeakingAttempt)
admin.site.register(WritingAttempt)
admin.site.register(CardReview)
