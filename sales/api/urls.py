from django.urls import path, include

urlpatterns = [
    path("mobile/", include("sales.api.mobile.urls")),
    path("admin/", include("sales.api.admin.urls")),
    path("inventory/", include("sales.api.inventory.urls")),
    path("web/", include("sales.api.web.urls"))
]
