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
    path("library/", views.library, name="library"),
    path("lesson/<int:pk>/", views.lesson_detail, name="lesson"),
    path("lesson/<int:pk>/complete/", views.lesson_complete, name="lesson_complete"),
]
