from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"offer", views.OfferAPI, basename="offer")
router.register(r"review", views.ReviewAPI, basename="review")
urlpatterns = [
    # path("global-settings/", views.GlobalSettingsAPI.as_view())
]
urlpatterns += router.urls
