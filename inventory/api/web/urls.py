from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"product", views.ProductAPI, basename="products")
router.register(r"category", views.CategoryAPI, basename="category")
router.register(r"attribute", views.AttributeAPI, basename="attribute")
router.register(r"attribute-value", views.AttributeValueAPI, basename="attribute-value")
router.register(r"tags", views.TagsAPI, basename="tags")
urlpatterns = [
    # path("global-settings/", views.GlobalSettingsAPI.as_view())
]
urlpatterns += router.urls
