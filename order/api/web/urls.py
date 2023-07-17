from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"billing-info", views.BIllingInfoAPI, basename="billing-info")
router.register(r"checkout", views.CheckoutAPI, basename="checkout")
router.register(r"verify-coupon", views.VerifyCouponAPI, basename="coupon")

urlpatterns = [
    # path("global-settings/", views.GlobalSettingsAPI.as_view())
]
urlpatterns += router.urls
