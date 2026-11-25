from django.contrib import admin, messages

from .models import Family, FamilyManager, Learner, PaymentRequest, PayoutRequest, ReferralEarning


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
    list_display = ("family", "paid_by", "plan", "display_amount", "amount_bdt", "method", "transaction_id",
                    "card_type", "status", "note", "created_at")
    list_filter = ("status", "method", "plan", "currency")
    search_fields = ("transaction_id", "bank_tran_id", "val_id", "family__name")
    readonly_fields = ("val_id", "bank_tran_id", "card_type")
    actions = ["confirm_payments"]

    @admin.action(description="Confirm selected payments (extends the family plan)")
    def confirm_payments(self, request, queryset):
        n = 0
        # An online payment can be confirmed by hand only after SSLCommerz validated it (it has a val_id).
        qs = queryset.filter(status=PaymentRequest.Status.PENDING).exclude(method=PaymentRequest.Method.SSLCOMMERZ, val_id="")
        for p in qs:
            p.confirm()
            n += 1
        self.message_user(request, f"{n} payment(s) confirmed.", messages.SUCCESS)


@admin.register(PayoutRequest)
class PayoutAdmin(admin.ModelAdmin):
    """Pay the family by bKash yourself, then set status to Paid and add the bKash TrxID as a note."""

    list_display = ("family", "amount_bdt", "bkash_number", "status", "created_at", "paid_at")
    list_filter = ("status",)
    list_editable = ("status",)

    def save_model(self, request, obj, form, change):
        from django.utils import timezone
        if obj.status == PayoutRequest.Status.PAID and not obj.paid_at:
            obj.paid_at = timezone.now()
        if obj.status == PayoutRequest.Status.REJECTED:
            obj.earnings.update(payout=None)  # money goes back to the family's balance
        super().save_model(request, obj, form, change)


@admin.register(ReferralEarning)
class ReferralEarningAdmin(admin.ModelAdmin):
    list_display = ("family", "from_family", "amount_bdt", "available_on", "payout")
