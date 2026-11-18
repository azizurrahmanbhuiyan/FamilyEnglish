from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "FamilyEnglish admin"
admin.site.site_title = "FamilyEnglish"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("learn/", include("learning.urls")),
    path("", include("core.urls")),
]
