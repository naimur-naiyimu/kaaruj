from django.urls import path, include

urlpatterns = [
    path("mobile/", include("promotions.api.mobile.urls")),
    path("admin/", include("promotions.api.admin.urls")),
    path("web/", include("promotions.api.web.urls"))
]
