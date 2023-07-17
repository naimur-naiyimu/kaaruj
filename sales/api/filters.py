import django_filters
from ..models import *
# https://www.youtube.com/watch?v=FTUxl5ZCMb8&ab_channel=BugBytes
class InvoiceFilter(django_filters.FilterSet):
    class Meta:
        model = Invoice
        fields = {
            'number': ['icontains'],
            'created_by__first_name': ['icontains'],
            'total_amount': ['icontains'],
            'created_at': ['lt', 'gt'],
            'updated_at': ['lt', 'gt'],
        }
        

class InvoiceSearchFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='my_custom_filter', label="search")
    to_mobile = django_filters.CharFilter(method='to_mobile_filter', label="to_mobile")

    class Meta:
        model = Invoice
        fields = ['query','created_for']

    def my_custom_filter(self, queryset, name, filter_by):
        return queryset.filter(is_custom=False).filter( Q(created_by__first_name__icontains=filter_by) | Q(created_by__last_name__icontains=filter_by) | Q(total_amount__icontains=filter_by) | Q(number__icontains=filter_by))

    def to_mobile_filter(self, queryset, name, filter_by):
        return queryset.filter(to_mobile__icontains=filter_by)


class CustomInvoiceSearchFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='my_custom_filter', label="search")

    class Meta:
        model = Invoice
        fields = ['query']

    def my_custom_filter(self, queryset, name, filter_by):
        return queryset.filter(is_custom=True).filter( Q(created_by__first_name__icontains=filter_by) | Q(created_by__last_name__icontains=filter_by) | Q(total_amount__icontains=filter_by) | Q(number__icontains=filter_by))
