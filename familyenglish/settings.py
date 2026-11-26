"""
Django settings for the FamilyEnglish project.

Development defaults are safe to run locally. For production, set the
FE_* settings in .env (see .env.example). All settings use the FE_
prefix so variables from other projects on the same machine are never picked up.
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_env_file(path):
    """Load KEY=VALUE lines from a .env file (used on cPanel hosting). The project .env wins."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ[key.strip()] = value.strip().strip('"').strip("'")


_load_env_file(BASE_DIR / ".env")

SECRET_KEY = os.environ.get(
    "FE_SECRET_KEY",
    "dev-only-change-me-familyenglish-0b7c1e9f4a2d",
)
DEBUG = os.environ.get("FE_DEBUG", "1") == "1"
ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get("FE_ALLOWED_HOSTS", "localhost,127.0.0.1,10.0.2.2").split(",")
    if h.strip()
]
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get("FE_CSRF_TRUSTED_ORIGINS", "").split(",")
    if o.strip()
]

if not DEBUG:
    # Behind cPanel's Apache/Passenger, which terminates HTTPS.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = os.environ.get("FE_SSL_REDIRECT", "1") == "1"
    SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
    CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "learning",
    "practice",
    "course",
    "growth",
    "studio",
    "rest_framework",
    "rest_framework.authtoken",
    "api",
    "world",
    "talk",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "core.middleware.DeviceMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "familyenglish.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.family_context",
                "practice.context_processors.practice_context",
                "growth.context_processors.growth_context",
                "studio.context_processors.studio_bar",
                "world.middleware.world_context",
            ],
        },
    },
]

WSGI_APPLICATION = "familyenglish.wsgi.application"

# PostgreSQL when FE_DB_NAME is set (production); SQLite otherwise (local development).
# The FE_ prefix keeps other projects' DB_* variables on the same machine from being picked up.
if os.environ.get("FE_DB_NAME"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["FE_DB_NAME"],
            "USER": os.environ.get("FE_DB_USER", ""),
            "PASSWORD": os.environ.get("FE_DB_PASSWORD", ""),
            "HOST": os.environ.get("FE_DB_HOST", "localhost"),
            "PORT": os.environ.get("FE_DB_PORT", "5432"),
            "CONN_MAX_AGE": 60,
            "CONN_HEALTH_CHECKS": True,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Dhaka"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        if DEBUG
        else "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "core:login"
LOGIN_REDIRECT_URL = "core:profiles"
LOGOUT_REDIRECT_URL = "core:home"

# FamilyEnglish product settings
FAMILY_MAX_LEARNERS = 6
FREE_TRIAL_DAYS = int(os.environ.get("FE_FREE_TRIAL_DAYS", "60"))  # every family gets everything free for 60 days from sign-up
# Optional: give families who joined earlier their free days from this date (YYYY-MM-DD). Empty = from sign-up only.
FREE_TRIAL_FROM = os.environ.get("FE_FREE_TRIAL_FROM", "")
if len(sys.argv) > 1 and sys.argv[1] == "test":
    FREE_TRIAL_DAYS = 0  # the tests check the free/paid lock rules; the free month has its own test

# Lesson days follow the Bangladesh school week (Sun-Thu). Python weekday(): Mon=0 ... Sun=6
DEFAULT_STUDY_WEEKDAYS = [6, 0, 1, 2, 3]

# Refer & earn
REFERRAL_EXTRA_TRIAL_DAYS = 7      # a family that joins with a code gets 14 + 7 trial days
REFERRAL_REWARD_DAYS = 30          # the inviting family gets 30 free days when the new family first pays
REFERRAL_COMMISSION_PCT = int(os.environ.get("FE_REFERRAL_COMMISSION_PCT", "10"))  # 0 switches it off
REFERRAL_HOLD_DAYS = 7             # commission can be withdrawn 7 days after the payment is confirmed
REFERRAL_MIN_PAYOUT = 500          # taka

# Free YouTube Data API key: finds short, on-topic clips for every lesson (python manage.py find_clips)
YOUTUBE_API_KEY = os.environ.get("FE_YOUTUBE_API_KEY", "")

# Optional links for the floating help button
MESSENGER_URL = os.environ.get("FE_MESSENGER_URL", "")

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
SUPPORT_MAX_UPLOAD_MB = 3

# AI tutor, writing helper and speaking feedback (optional).
# Without FE_AI_API_KEY everything still works with built-in, rule-based feedback.
AI_API_KEY = os.environ.get("FE_AI_API_KEY", "")
AI_MODEL = os.environ.get("FE_AI_MODEL", "claude-haiku-5-5")
AI_DAILY_LIMIT = int(os.environ.get("FE_AI_DAILY_LIMIT", "20"))   # AI replies per learner per day
TALK_AI_DAILY_LIMIT = int(os.environ.get("FE_TALK_AI_DAILY_LIMIT", "60"))  # AI calls per learner per day in Talk lessons
# The AI level test uses a stronger model to mark writing and speaking and to write the report.
AI_TEST_MODEL = os.environ.get("FE_AI_TEST_MODEL", "claude-sonnet-5-5")


# ---------------------------------------------------------------- mobile app API (/api/v1/)
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.TokenAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_THROTTLE_RATES": {"anon": "30/min", "user": "120/min"},
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.UserRateThrottle"],
}


# ---------------------------------------------------------------- going global (v15)
# Families outside Bangladesh get full access free for now (they cannot pay by bKash/Nagad yet).
FE_FREE_OUTSIDE_BD = os.environ.get("FE_FREE_OUTSIDE_BD", "0") == "1"  # 0 = everyone pays

# Email (sign-up and sign-in codes). On cPanel: create noreply@yourdomain in "Email Accounts" and put its
# details in .env. Without them, emails are printed in the server log (fine for testing on your PC).
EMAIL_HOST = os.environ.get("FE_EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("FE_EMAIL_PORT", "465"))
EMAIL_HOST_USER = os.environ.get("FE_EMAIL_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("FE_EMAIL_PASSWORD", "")
EMAIL_USE_SSL = EMAIL_PORT == 465
EMAIL_USE_TLS = EMAIL_PORT == 587
EMAIL_TIMEOUT = 20
EMAIL_BACKEND = ("django.core.mail.backends.smtp.EmailBackend" if EMAIL_HOST
                 else "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.environ.get("FE_EMAIL_FROM", EMAIL_HOST_USER or "FamilyEnglish <noreply@familyenglish.global>")

# SMS codes: "none" (email only), "bulksmsbd" (Bangladesh) or "twilio" (most countries).
# SSLCommerz payment gateway (https://sslcommerz.com). Empty = online payment hidden.
SSLC_STORE_ID = os.environ.get("FE_SSLC_STORE_ID", "")
SSLC_STORE_PASSWORD = os.environ.get("FE_SSLC_STORE_PASSWORD", "")
SSLC_SANDBOX = os.environ.get("FE_SSLC_SANDBOX", "1") == "1"   # 1 = test payments, 0 = real money

FE_SMS_BACKEND = os.environ.get("FE_SMS_BACKEND", "none")
FE_SMS_API_KEY = os.environ.get("FE_SMS_API_KEY", "")          # BulkSMSBD api_key / Twilio Account SID
FE_SMS_SECRET = os.environ.get("FE_SMS_SECRET", "")            # Twilio Auth Token
FE_SMS_SENDER = os.environ.get("FE_SMS_SENDER", "")            # BulkSMSBD senderid / Twilio from-number
