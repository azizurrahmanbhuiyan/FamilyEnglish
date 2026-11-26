from django.contrib.auth import views as auth_views
from django.urls import path

from world import views as world_views

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("pricing/", views.pricing, name="pricing"),
    path("privacy/", views.privacy, name="privacy"),
    path("worksheets/", views.worksheets, name="worksheets"),
    path("signup/", world_views.signup, name="signup"),
    path("login/", views.FamilyLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("family/new/", views.family_create, name="family_create"),
    path("family/", views.family, name="family"),
    path("family/password/", views.password, name="password"),
    path("family/pay/", views.pay, name="pay"),
    path("family/pay/online/", views.pay_online, name="pay_online"),
    path("family/pay/result/", views.pay_result, name="pay_result"),
    path("pay/sslcommerz/success/", views.sslc_success, name="sslc_success"),
    path("pay/sslcommerz/fail/", views.sslc_fail, name="sslc_fail"),
    path("pay/sslcommerz/cancel/", views.sslc_cancel, name="sslc_cancel"),
    path("pay/sslcommerz/ipn/", views.sslc_ipn, name="sslc_ipn"),
    path("family/managers/add/", views.manager_add, name="manager_add"),
    path("family/managers/<int:pk>/remove/", views.manager_remove, name="manager_remove"),
    path("who/", views.profiles, name="profiles"),
    path("who/switch/", views.switch_learner, name="switch"),
    path("who/<int:pk>/", views.choose_learner, name="choose"),
    path("learners/add/", views.learner_add, name="learner_add"),
    path("learners/<int:pk>/edit/", views.learner_edit, name="learner_edit"),
    path("learners/<int:pk>/delete/", views.learner_delete, name="learner_delete"),
]
