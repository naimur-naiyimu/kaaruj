from django.urls import path, include

urlpatterns = [
    path("mobile/", include("order.api.mobile.urls")),
    path("admin/", include("order.api.admin.urls")),
    path("web/", include("order.api.web.urls"))
]
