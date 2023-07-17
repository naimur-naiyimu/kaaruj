from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"contact-us", views.ContactUsWEBAPI, basename="contact-us")
router.register(r"page", views.PageAPI, basename="page")
# router.register(r"payment", views.PaymentAPI, basename="PaymentAPI")
router.register(r"social-media", views.SocialMediaAPI)
router.register(r"testimonial", views.TestimonialAdminAPI)
router.register(r"team-member", views.TeamMemberAPI)
router.register(r"display-center", views.DisplayCenterAPI)
router.register(r"subscription", views.subscription)

urlpatterns = [
    path("global-settings/", views.GlobalSettingsAPI.as_view())
    # path("payment/", views.PaymentAPI.as_view())
]
urlpatterns += router.urls
