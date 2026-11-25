"""Remember signed-in devices so a family can see them and sign out the others."""

from datetime import timedelta

from django.utils import timezone

UPDATE_EVERY = timedelta(minutes=5)


def device_label(user_agent):
    ua = (user_agent or "").lower()
    system = ("Android" if "android" in ua else "iPhone" if "iphone" in ua else "iPad" if "ipad" in ua
              else "Windows" if "windows" in ua else "Mac" if "mac os" in ua else "Linux" if "linux" in ua
              else "Device")
    browser = ("Edge" if "edg/" in ua else "Chrome" if "chrome" in ua else "Firefox" if "firefox" in ua
               else "Safari" if "safari" in ua else "Browser")
    return f"{browser} on {system}"


class DeviceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, "user", None)
        session = getattr(request, "session", None)
        if user is not None and user.is_authenticated and session is not None and session.session_key:
            from .models import UserDevice

            now = timezone.now()
            last = session.get("_device_seen")
            if not last or now.timestamp() - last > UPDATE_EVERY.total_seconds():
                UserDevice.objects.update_or_create(
                    session_key=session.session_key,
                    defaults={"user": user, "last_seen": now,
                              "label": device_label(request.META.get("HTTP_USER_AGENT"))[:120]})
                session["_device_seen"] = now.timestamp()
        return response
