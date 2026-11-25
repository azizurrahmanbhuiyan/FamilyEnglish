from django.urls import path

from . import views

app_name = "course"

urlpatterns = [
    path("", views.home, name="home"),
    path("level-test/", views.level_test, name="level_test"),
    path("level-test/start/", views.level_test_start, name="level_start"),
    path("level-test/<int:pk>/", views.level_step, name="level_step"),
    path("level-test/<int:pk>/result/", views.level_result, name="level_result"),
    path("path/plan/", views.path_plan, name="path_plan"),
    path("handbook/", views.handbook, name="handbook"),
    path("handbook/<int:n>.pdf", views.handout, name="handout"),
    path("check/", views.check, name="check"),
    path("weak-spots/", views.weak_spots, name="weak_spots"),
    path("drill/<str:qtype>/", views.drill, name="drill"),
    path("lesson/<slug:slug>/", views.lesson, name="lesson"),
    path("lesson/<slug:slug>/practice-done/", views.practice_done, name="practice_done"),
    path("lesson/<slug:slug>/self-test/", views.selftest, name="selftest"),
    path("self-test/<int:pk>/", views.result, name="result"),
    path("<str:skill>/", views.skill_page, name="skill"),
]
