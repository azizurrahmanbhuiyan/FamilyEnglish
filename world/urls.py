from django.urls import path

from . import views

app_name = "world"

urlpatterns = [
    path("language/", views.language, name="language"),
    path("verify/", views.verify, name="verify"),
    path("verify/resend/", views.resend, name="resend"),
    path("login/code/", views.login_code, name="login_code"),
]
