"""SSLCommerz payment gateway (API v4): card, bKash/Nagad/Rocket, internet banking; BDT or USD.

Flow:
1. pay_online creates a pending PaymentRequest and asks SSLCommerz for a session (start()).
2. The family pays on the SSLCommerz page.
3. SSLCommerz posts to success / fail / cancel (the browser) and to the IPN URL (server to server).
4. We never trust those posts: we call the order validation API with the val_id and confirm only when the
   status is VALID/VALIDATED and the transaction, currency and amount are exactly ours (settle()).

Settings (.env): FE_SSLC_STORE_ID, FE_SSLC_STORE_PASSWORD, FE_SSLC_SANDBOX (1 = test, 0 = live).
"""

import json
import logging
import secrets
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.db import transaction
from django.urls import reverse

log = logging.getLogger(__name__)
OK_STATUSES = {"VALID", "VALIDATED"}


class GatewayError(Exception):
    pass


def enabled():
    return bool(settings.SSLC_STORE_ID and settings.SSLC_STORE_PASSWORD)


def _base():
    return "https://sandbox.sslcommerz.com" if settings.SSLC_SANDBOX else "https://securepay.sslcommerz.com"


def _post(url, data):  # pragma: no cover - network
    body = urllib.parse.urlencode(data).encode()
    with urllib.request.urlopen(urllib.request.Request(url, data=body, method="POST"), timeout=30) as r:
        return json.loads(r.read().decode())


def _get(url, params):  # pragma: no cover - network
    with urllib.request.urlopen(url + "?" + urllib.parse.urlencode(params), timeout=30) as r:
        return json.loads(r.read().decode())


def new_tran_id():
    return "FE" + secrets.token_hex(9).upper()


def start(payment, request):
    """Create a gateway session for this pending payment and return the page to send the family to."""
    from world.data import country as country_info
    from world.models import Profile

    user = payment.paid_by
    profile = Profile.objects.filter(user=user).first()
    iso = payment.family.country or "BD"
    cname = (country_info(iso) or {}).get("name", iso) if iso else "Bangladesh"
    url = lambda name: request.build_absolute_uri(reverse(name))  # noqa: E731
    data = {
        "store_id": settings.SSLC_STORE_ID,
        "store_passwd": settings.SSLC_STORE_PASSWORD,
        "total_amount": f"{payment.amount:.2f}",
        "currency": payment.currency,
        "tran_id": payment.transaction_id,
        "success_url": url("core:sslc_success"),
        "fail_url": url("core:sslc_fail"),
        "cancel_url": url("core:sslc_cancel"),
        "ipn_url": url("core:sslc_ipn"),
        "cus_name": (user.get_full_name() or user.first_name or payment.family.name)[:50] or "FamilyEnglish family",
        "cus_email": user.email or "noreply@familyenglish.global",
        "cus_add1": cname,
        "cus_city": cname,
        "cus_postcode": "0000",
        "cus_country": cname,
        "cus_phone": (profile.phone if profile and profile.phone else "N/A"),
        "shipping_method": "NO",
        "num_of_item": 1,
        "product_name": f"FamilyEnglish {payment.get_plan_display()}",
        "product_category": "Education",
        "product_profile": "non-physical-goods",
        "value_a": str(payment.pk),
        "value_b": str(payment.family_id),
    }
    try:
        res = _post(_base() + "/gwprocess/v4/api.php", data)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        log.warning("SSLCommerz session failed: %s", exc)
        raise GatewayError("The payment service did not answer. Please try again.") from exc
    if res.get("status") != "SUCCESS" or not res.get("GatewayPageURL"):
        log.warning("SSLCommerz session refused: %s", res.get("failedreason"))
        raise GatewayError(res.get("failedreason") or "The payment service refused the request.")
    return res["GatewayPageURL"]


def validate(val_id):
    try:
        return _get(_base() + "/validator/api/validationserverAPI.php", {
            "val_id": val_id, "store_id": settings.SSLC_STORE_ID,
            "store_passwd": settings.SSLC_STORE_PASSWORD, "format": "json"})
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        log.warning("SSLCommerz validation failed: %s", exc)
        return None


def _money(v):
    try:
        return Decimal(str(v)).quantize(Decimal("0.01"))
    except (InvalidOperation, TypeError):
        return None


def settle(tran_id, val_id):
    """Check a payment with SSLCommerz and confirm it once. Returns the PaymentRequest (or None)."""
    from .models import PaymentRequest

    if not tran_id or not val_id:
        return None
    data = validate(val_id)
    with transaction.atomic():
        p = (PaymentRequest.objects.select_for_update()
             .filter(transaction_id=tran_id, method=PaymentRequest.Method.SSLCOMMERZ).first())
        if p is None or p.status == PaymentRequest.Status.CONFIRMED:
            return p
        if not data:
            # SSLCommerz did not answer: keep the val_id so the result page / IPN can check again.
            p.val_id, p.note = val_id[:80], "Validation: no answer yet, will retry"
            p.save(update_fields=["val_id", "note"])
            return p
        if data.get("status") not in OK_STATUSES:
            p.note = f"Validation: {data.get('status', '?')}"[:200]
            p.save(update_fields=["note"])
            return p
        cur = (data.get("currency_type") or data.get("currency") or "").upper()
        paid = _money(data.get("currency_amount") or data.get("amount"))
        if data.get("tran_id") != p.transaction_id or cur != p.currency or paid != _money(p.amount):
            p.status, p.note = PaymentRequest.Status.REJECTED, f"Mismatch: {cur} {paid} for {p.currency} {p.amount}"
            p.save(update_fields=["status", "note"])
            log.error("SSLCommerz mismatch for %s: %s", tran_id, data)
            return p
        p.val_id = val_id[:80]
        p.bank_tran_id = (data.get("bank_tran_id") or "")[:80]
        p.card_type = (data.get("card_type") or "")[:60]
        bdt = _money(data.get("amount") if cur != "BDT" else paid)
        if bdt is not None and p.currency != "BDT":
            p.amount_bdt = int(bdt)
        # Paid and validated: the family gets access straight away, no manual approval.
        # A payment SSLCommerz marks as high risk is still confirmed, with a note for the admin to look at.
        p.note = (f"High risk: {data.get('risk_title', '')} — review in the SSLCommerz panel"[:200]
                  if str(data.get("risk_level", "0")) == "1" else "")
        p.save()
        p.confirm()
    return p


def mark(tran_id, status):
    """Record a failed or cancelled payment (only while it is still pending)."""
    from .models import PaymentRequest

    PaymentRequest.objects.filter(transaction_id=tran_id, method=PaymentRequest.Method.SSLCOMMERZ,
                                  status=PaymentRequest.Status.PENDING).update(status=status)
