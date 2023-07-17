from django.urls import path, include

urlpatterns = [
    path("mobile/", include("inventory.api.mobile.urls")),
    path("admin/", include("inventory.api.admin.urls")),
    path("inventory/", include("inventory.api.inventory.urls")),
    path("web/", include("inventory.api.web.urls"))
]
