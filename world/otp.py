"""Send 6-digit sign-up and sign-in codes by email, and by SMS when an SMS service is set up.

SMS is switched off until you choose a provider in .env:
    FE_SMS_BACKEND=bulksmsbd   FE_SMS_API_KEY=...  FE_SMS_SENDER=...            (Bangladesh)
    FE_SMS_BACKEND=twilio      FE_SMS_API_KEY=<Account SID>  FE_SMS_SECRET=<Auth Token>  FE_SMS_SENDER=<+1 number>
Check your provider's current API page once before going live — providers sometimes change their URLs.
"""

import base64
import json
import logging
import urllib.parse
import urllib.request
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import OneTimeCode, Profile
from .translate import text

log = logging.getLogger(__name__)
RESEND_AFTER = timedelta(seconds=60)
MAX_PER_HOUR = 5


def mask_email(email):
    name, _, domain = (email or "").partition("@")
    return (name[:2] + "•••@" + domain) if domain else ""


def mask_phone(phone):
    return phone[:-6] + "•••" + phone[-3:] if len(phone or "") > 8 else phone


def sms_enabled():
    return settings.FE_SMS_BACKEND in ("bulksmsbd", "twilio") and bool(settings.FE_SMS_API_KEY)


def can_send(user):
    """(ok, seconds to wait). One code a minute, five an hour."""
    now = timezone.now()
    recent = OneTimeCode.objects.filter(user=user, created_at__gte=now - timedelta(hours=1))
    last = recent.first()
    if last and now - last.created_at < RESEND_AFTER:
        return False, int((RESEND_AFTER - (now - last.created_at)).total_seconds()) + 1
    if recent.count() >= MAX_PER_HOUR:
        return False, 3600
    return True, 0


def send_code(user, purpose, lang="en"):
    """Create a code and send it to the account's email (and mobile when SMS is on). Returns (otp, places)."""
    profile = Profile.objects.filter(user=user).first()
    places = []
    if user.email:
        places.append(mask_email(user.email))
    phone = profile.phone if profile else ""
    if phone and sms_enabled():
        places.append(mask_phone(phone))
    otp, code = OneTimeCode.issue(user, purpose, ", ".join(places))
    msg = text("Your FamilyEnglish code is", lang) + f" {code}. " + text("It works for 10 minutes. Do not share it with anyone.", lang)
    if user.email:
        try:
            send_mail(f"{code} — " + text("your FamilyEnglish code", lang),
                      msg + "\n\n" + text("If you did not ask for this code, you can ignore this email.", lang) + "\n\nFamilyEnglish",
                      None, [user.email], fail_silently=False)
        except Exception:  # pragma: no cover - mail server problems
            log.exception("Could not email the sign-in code")
    if phone and sms_enabled():
        try:
            send_sms(phone, f"FamilyEnglish: {code}. " + text("It works for 10 minutes. Do not share it with anyone.", lang))
        except Exception:  # pragma: no cover - SMS provider problems
            log.exception("Could not send the sign-in code by SMS")
    return otp, places


def send_sms(phone, body):
    backend = settings.FE_SMS_BACKEND
    if backend == "bulksmsbd":
        q = urllib.parse.urlencode({"api_key": settings.FE_SMS_API_KEY, "type": "text", "number": phone.lstrip("+"),
                                    "senderid": settings.FE_SMS_SENDER, "message": body})
        with urllib.request.urlopen(f"https://bulksmsbd.net/api/smsapi?{q}", timeout=15) as r:
            return r.read()
    if backend == "twilio":
        sid, token = settings.FE_SMS_API_KEY, settings.FE_SMS_SECRET
        data = urllib.parse.urlencode({"To": phone, "From": settings.FE_SMS_SENDER, "Body": body}).encode()
        req = urllib.request.Request(f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json", data=data)
        req.add_header("Authorization", "Basic " + base64.b64encode(f"{sid}:{token}".encode()).decode())
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read() or b"{}")
    return None
