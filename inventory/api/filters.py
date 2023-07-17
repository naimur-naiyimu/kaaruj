from django_filters import rest_framework as rest_filter
from ..models import *
from rest_framework import serializers
from ..constants import *
class ProductFilter(rest_filter.FilterSet):
    min_price = rest_filter.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = rest_filter.NumberFilter(field_name='price', lookup_expr='lte')
    is_offer  = rest_filter.BooleanFilter(
        field_name="client",
        method="filter_is_offer",
        label="is_offer",
    )
    sort_by = rest_filter.ChoiceFilter(method='filter_sort_by', choices=ProductSortChoices.choices, label="Sort by (0:Popularity, 1:Rating, 2:Latest, 3:Price Low to High, 4:Price High to Low)")
    sort_by_attribute = rest_filter.CharFilter(method='filter_sort_by_attribute', label="Sort by attribute")
    class Meta:
        model = Products
        fields = ['min_price', 'max_price','category','main_category' ,'tags', 'variant','is_new_arrival','price']


    def filter_is_offer(self, queryset, name, value):
        products = queryset.filter(offer__isnull=False)
        return products
    
    def filter_sort_by(self, queryset, name, value):
        value = str(value)
        if value == str(ProductSortChoices.POPULARITY):

            products =  queryset.annotate(total_sold=Sum('invoice_products__quantity')).order_by('-total_sold')
            # for product in products:
            #     print(product.name, product.total_sold)
            return products
        elif value == str(ProductSortChoices.RATING):
            return queryset.annotate(avg_rating=Avg('review__star')).order_by('-avg_rating')
        elif value == str(ProductSortChoices.LATEST):
            return queryset.order_by('-created_at')
        elif value == str(ProductSortChoices.PRICE_LOW_TO_HIGH):
            return queryset.order_by('price')
        elif value ==str(ProductSortChoices.PRICE_HIGH_TO_LOW):
            return queryset.order_by('-price')
        else:
            return queryset.order_by('-created_at')
        
    def filter_sort_by_attribute(self, queryset, name, value):
        ids = value.split(',')
        return queryset.filter(variant__attribute_value__id__in=ids).distinct()
    


class AttributeFilter(rest_filter.FilterSet):
    product = rest_filter.CharFilter(method='filter_by_product', label="filter_by_product")
    class Meta:
        model = Attributes
        fields = '__all__'
 
        
    def filter_by_product(self, queryset, name, value):
        pass
    
class TagsFilter(rest_filter.FilterSet):
    category = rest_filter.ChoiceFilter(method='filter_by_product', choices=MainCategoryChoices.choices, label="Sort by (0:Home Decor, 1:In Style)")
    class Meta:
        model = Tags
        fields = '__all__'
 
        
    def filter_by_product(self, queryset, name, value):
        prods = Products.objects.filter(main_category=int(value))
        tags = []
        for prod in prods:
            for tag in prod.tags.all():
                tags.append(tag.id)
        return queryset.filter(id__in=tags).distinct()
        
