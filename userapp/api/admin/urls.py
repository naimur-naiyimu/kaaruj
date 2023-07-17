from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
# router.register(r"product", views.ProductApi, basename="products")

urlpatterns = [
    # path("<int:user>/product/<int:id>/", views.ProductGetApi.as_view()),
]
urlpatterns += router.urls
