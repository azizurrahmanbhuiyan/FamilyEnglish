from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "FamilyEnglish admin"
admin.site.site_title = "FamilyEnglish"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("learn/", include("learning.urls")),
    path("practice/", include("practice.urls")),
    path("course/", include("course.urls")),
    path("me/", include("growth.urls")),
    path("app/", include("studio.urls")),
    path("talk/", include("talk.urls")),
    path("api/v1/", include("api.urls")),
    path("", include("world.urls")),
    path("", include("core.urls")),
]
