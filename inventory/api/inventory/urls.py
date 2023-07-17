from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.api.inventory.views import *
from inventory.api.inventory import views
router = DefaultRouter()
router.register(r'attributes', AttributeViewSet, basename='attribute')
router.register(r'products', ProductView, basename='products')
# router.register(r'products-image', ProductImagesView, basename='products-images')
router.register(r'variant', ProductVariantView, basename='products-variants')
router.register(r'category', CategoryView, basename='category')
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'product_list_for_invoice', views.ProductViewForInvoice, basename='ProductViewForInvoice')
urlpatterns = [
    path('bulk-export/', BulkExportView.as_view()),
    path('bulk-import/', views.ProductBulkImportAPI.as_view()),
    path('bulk-import/customer/', views.CustomerBulkImportView.as_view()),
    path('variant-update/', views.productUpdateView.as_view()),
    # path('product_barcode/', views.ProductBarcodePrint.as_view()),
    path('product_barcode/', views.ProductImageBase64.as_view()),
    path('customer_list_for_invoice/', views.CustomerViewForInvoice.as_view()),
    path('export/products/', views.ExportProductAPIView.as_view()),
    path('export/customer/', views.ExportCustomerAPIView.as_view()),


]
urlpatterns += router.urls
