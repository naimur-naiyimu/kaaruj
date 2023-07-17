from django.urls import path, include

urlpatterns = [
    path("mobile/", include("userapp.api.mobile.urls")),
    path("admin/", include("userapp.api.admin.urls")),
    path("inventory/", include("userapp.api.inventory.urls")),
    path("web/", include("userapp.api.web.urls"))
]
