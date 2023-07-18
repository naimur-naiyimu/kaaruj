from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'invoice', views.InvoiceViewSet, basename='invoice')
router.register(r'all-invoice', views.AllInvoiceView, basename='all-invoice')
router.register(r'custom-invoice', views.CustomInvoiceView, basename='custom-invoice')
urlpatterns = [
    path('invoice-products/', views.InvoiceNewProductsView.as_view()),
    # path('invoice-products/update/', views.InvoiceNewProductsViewForEdit.as_view()),
    path('daily-report/', views.GetDailyReport.as_view()),
    path('create-daily-report/', views.createDailyReportFromAPi.as_view()),
    path('daily-report/<int:pk>', views.DeleteDailyReport.as_view()),
    path('chart_data1/', views.ReportChartData.as_view()),
    path('chart_data_invoice_created/', views.ChartDataInvoiceByCreated.as_view()),
    path('chart_data_customer_created/', views.ChartDataCustomer.as_view()),
    path('generate_pdf/', views.SaveAndSendPdf.as_view()),
    path('export/daily-report/', views.ExportDailyReportAPIView.as_view()),
    path('daily-sales-report', views.DailySalesReportAPIView.as_view()),
    path('inventory/notifications', views.NotificationView.as_view()),

]+router.urls

