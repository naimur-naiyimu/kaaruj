from django.urls import path, include

app_name = 'api-v1'

urlpatterns = [
    path('auth/', include('coreapp.api.urls')),
    path('utility/', include('utility.api.urls')),
    path('inventory/', include('inventory.api.urls')),
    path('promotions/', include('promotions.api.urls')),
    path('order/', include('order.api.urls')),
    path('sales/', include('sales.api.urls')),
    path('users/', include('userapp.api.urls')),
]
