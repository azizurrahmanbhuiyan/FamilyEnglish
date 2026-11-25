from django.contrib import admin

from .models import OneTimeCode, Profile, UiText


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "phone", "language", "email_verified", "phone_verified", "created_at")
    list_filter = ("country", "language", "email_verified", "phone_verified")
    search_fields = ("user__email", "phone")


@admin.register(OneTimeCode)
class OneTimeCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "purpose", "sent_to", "attempts", "used", "created_at", "expires_at")
    readonly_fields = ("code_hash",)


@admin.register(UiText)
class UiTextAdmin(admin.ModelAdmin):
    list_display = ("lang", "source", "text", "origin", "updated_at")
    list_filter = ("lang", "origin")
    search_fields = ("source", "text")
    list_editable = ("text",)

    def save_model(self, request, obj, form, change):
        if obj.text:
            obj.origin = UiText.Origin.MANUAL
        super().save_model(request, obj, form, change)
        from .translate import forget
        forget(obj.lang)
