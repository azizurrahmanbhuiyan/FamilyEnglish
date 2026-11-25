from django.urls import path

from . import talk, views

app_name = "api"

urlpatterns = [
    path("auth/login/", views.login, name="login"),
    path("auth/logout/", views.logout, name="logout"),
    path("me/", views.me, name="me"),
    path("today/", views.today, name="today"),
    path("units/", views.units, name="units"),
    path("units/<slug:slug>/", views.unit_detail, name="unit"),
    path("grammar/", views.grammar_list, name="grammar"),
    path("attempt/", views.attempt, name="attempt"),
    path("finish/", views.finish, name="finish"),
    path("shorts/", views.shorts, name="shorts"),
    path("shorts/try/", views.short_try, name="short_try"),
    path("progress/", views.progress, name="progress"),
    path("dictionary/", views.dictionary, name="dictionary"),
    path("talk/profile/", talk.profile, name="talk_profile"),
    path("talk/home/", talk.home, name="talk_home"),
    path("talk/roleplays/", talk.roleplays, name="talk_roleplays"),
    path("talk/read/", talk.library, name="talk_library"),
    path("talk/read/<slug:slug>/", talk.article, name="talk_article"),
    path("talk/start/", talk.start, name="talk_start"),
    path("talk/<int:pk>/reply/", talk.reply, name="talk_reply"),
    path("talk/<int:pk>/hint/", talk.hint, name="talk_hint"),
    path("talk/<int:pk>/translate/", talk.translate, name="talk_translate"),
    path("talk/<int:pk>/finish/", talk.finish, name="talk_finish"),
    path("talk/<int:pk>/practice/", talk.practice, name="talk_practice"),
]
