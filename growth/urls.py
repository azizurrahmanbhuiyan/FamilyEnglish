from django.urls import path

from . import views

app_name = "growth"

urlpatterns = [
    path("streaks/", views.streaks, name="streaks"),
    path("goals/", views.goals, name="goals"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("profile/", views.profile, name="profile"),
    path("devices/sign-out-others/", views.signout_others, name="signout_others"),
    path("ideas/", views.ideas, name="ideas"),
    path("ideas/<int:pk>/vote/", views.vote, name="vote"),
    path("whats-new/", views.whats_new, name="whats_new"),
    path("lang/<str:code>/", views.set_language, name="lang"),
]
