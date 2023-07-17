import django_filters
from inventory.models import *
from utility.utils import filter_utils
from django.db.models import *
# https://www.youtube.com/watch?v=FTUxl5ZCMb8&ab_channel=BugBytes
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Products
        fields = {
            'name': ['icontains'],
            'category__name': ['icontains'],
            'sku': ['icontains'],
            'created_at': ['lt', 'gt'],
            'updated_at': ['lt', 'gt'],
        }

class ProductSearchFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='my_custom_filter', label="search")
    filter = django_filters.CharFilter(method='day_month_filter', label="filter")
    dates = django_filters.CharFilter(method='date_range_filter', label="dates")

    class Meta:
        model = Products
        fields = ['query']

    def my_custom_filter(self, queryset, name, filter_by):
        return queryset.filter( Q(category__name__icontains=filter_by) | Q(name__icontains=filter_by) | Q(sku__icontains=filter_by))

    def day_month_filter(self, queryset, name, filter_by):
        if (filter_by == "today"):
            return filter_utils.todays_queryset(Products)
                
        if (filter_by == "week"):
            return filter_utils.weekly_queryset(Products)

        if (filter_by == "month"):
            print("month",filter_utils.monthly_queryset(Products))
            return filter_utils.monthly_queryset(Products)

        if (filter_by == "year"):
            return filter_utils.yearly_queryset(Products)
        if (filter_by == "all"):
            return  Products.objects.all().order_by("-created_at")
        return queryset
    
    def date_range_filter(self, queryset, name, dates):
        start,end = dates.split(",")
        start_month, start_day,  start_year = start.split("/")
        end_month, end_day,  end_year = end.split("/")

        start_date = datetime.datetime(year=int(start_year), month=int(start_month), day=int(start_day),
                                        hour=0, minute=0, second=0)  # represents 00:00:00
        end_date = datetime.datetime(year=int(end_year), month=int(end_month), day=int(end_day),
                                        hour=23, minute=59, second=59)
        return Products.objects.filter(updated_at__range=[start_date, end_date])
    


class CustomerFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='my_custom_filter', label="search")
    filter = django_filters.CharFilter(method='day_month_filter', label="filter")
    
    class Meta:
        model = Customer
        fields = ['query','filter']

    def my_custom_filter(self, queryset, name, filter_by):
        return queryset.filter( Q(name__icontains=filter_by) | Q(mobile__icontains=filter_by) | Q(email__icontains=filter_by))

    def day_month_filter(self, queryset, name, filter_by):
        if (filter_by == "today"):
            return filter_utils.todays_queryset(Customer)
                
        if (filter_by == "week"):
            return filter_utils.weekly_queryset(Customer)

        if (filter_by == "month"):
            return filter_utils.monthly_queryset(Customer)

        if (filter_by == "year"):
            return filter_utils.yearly_queryset(Customer)
        if (filter_by == "all"):
            return  Customer.objects.all().order_by("-created_at")
        return queryset
    
 
   