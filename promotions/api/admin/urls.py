from django.urls import path
from rest_framework import routers

from . import views
from order.api.admin import views as order_views

router = routers.DefaultRouter()
router.register(r"review", views.ReviewAPI, basename="review")
router.register(r"offer", views.OfferAPI, basename="offer")
router.register(r"coupon", order_views.CouponAPI, basename="coupon")

urlpatterns = [
    # path("global-settings/", views.GlobalSettingsAPI.as_view())
]
urlpatterns += router.urls
