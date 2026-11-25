from django.urls import path

from . import views

app_name = "learning"

urlpatterns = [
    path("", views.today, name="today"),
    path("placement/", views.placement_start, name="placement_start"),
    path("placement/young/", views.placement_young, name="placement_young"),
    path("placement/reader/", views.placement_reader, name="placement_reader"),
    path("placement/result/<int:pk>/", views.placement_result, name="placement_result"),
    path("plan/", views.plan_calendar, name="plan"),
    path("plan/new/", views.plan_new, name="plan_new"),
    path("plan/day/<int:pk>/done/", views.day_done, name="day_done"),
    path("plan/day/<int:pk>/", views.plan_day, name="plan_day"),
    path("plan/restart/", views.plan_restart, name="plan_restart"),
    path("lesson/<int:pk>/watched/", views.video_watched, name="video_watched"),
    path("lesson/<int:pk>/talk/<str:who>/said/", views.talk_said, name="talk_said"),
    path("lesson/<int:pk>/talk/ai/", views.talk_ai, name="talk_ai"),
    path("talk/", views.talk_hub, name="talk_hub"),
    path("talk/<slug:slug>/", views.talk_topic, name="talk_topic"),
    path("talk/<slug:slug>/said/<str:who>/", views.topic_said, name="topic_said"),
    path("talk/<slug:slug>/ai/", views.topic_ai, name="topic_ai"),
    path("library/", views.library, name="library"),
    path("phonics-year/", views.phonics_year, name="phonics_year"),
    path("phonics-year/week/<int:n>/", views.phonics_week, name="phonics_week"),
    path("videos/", views.videos, name="videos"),
    path("progress/", views.progress, name="progress"),
    path("lesson/<int:pk>/", views.lesson_detail, name="lesson"),
    path("lesson/<int:pk>/complete/", views.lesson_complete, name="lesson_complete"),
]
