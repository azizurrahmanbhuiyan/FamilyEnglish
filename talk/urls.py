from django.urls import path

from . import views

app_name = "talk"

urlpatterns = [
    path("", views.home, name="home"),
    path("setup/", views.setup, name="setup"),
    path("go/<str:kind>/", views.go, name="go"),
    path("go/<str:kind>/<slug:ref>/", views.go, name="go_ref"),
    path("roleplays/", views.roleplays, name="roleplays"),
    path("read/", views.read, name="read"),
    path("read/<slug:slug>/", views.article, name="article"),
    path("s/<int:pk>/", views.chat, name="chat"),
    path("s/<int:pk>/report/", views.report, name="report"),
    path("api/<int:pk>/reply/", views.api_reply, name="api_reply"),
    path("api/<int:pk>/hint/", views.api_hint, name="api_hint"),
    path("api/<int:pk>/translate/", views.api_translate, name="api_translate"),
    path("api/<int:pk>/finish/", views.api_finish, name="api_finish"),
    path("api/<int:pk>/practice/", views.api_practice, name="api_practice"),
]
