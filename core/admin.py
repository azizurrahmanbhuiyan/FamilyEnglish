from django.contrib import admin, messages

from .models import Family, FamilyManager, Learner, PaymentRequest


class LearnerInline(admin.TabularInline):
    model = Learner
    extra = 0
    fields = ("avatar", "name", "role", "birth_year", "daily_limit_minutes")


class ManagerInline(admin.TabularInline):
    model = FamilyManager
    extra = 0


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "plan", "paid_until", "created_at")
    list_filter = ("plan",)
    search_fields = ("name", "owner__email")
    inlines = [ManagerInline, LearnerInline]


@admin.register(PaymentRequest)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("family", "paid_by", "plan", "amount_bdt", "method", "transaction_id",
                    "status", "created_at")
    list_filter = ("status", "method", "plan")
    search_fields = ("transaction_id", "family__name")
    actions = ["confirm_payments"]

    @admin.action(description="Confirm selected payments (extends the family plan)")
    def confirm_payments(self, request, queryset):
        n = 0
        for p in queryset.filter(status=PaymentRequest.Status.PENDING):
            p.confirm()
            n += 1
        self.message_user(request, f"{n} payment(s) confirmed.", messages.SUCCESS)
