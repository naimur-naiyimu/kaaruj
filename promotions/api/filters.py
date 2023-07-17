from django_filters import rest_framework as filters
from ..models import *
from restaurant.models import *
from rest_framework import serializers
class ProductFilter(filters.FilterSet):
    client = filters.CharFilter(
        field_name="client",
        method="filter_client_product",
        label="client",
    )

    
    choice = filters.CharFilter(
        field_name="choice",
        method="filter_product_choice",
        label='''
        1 : Top Rated \n
        2 : Today's Special \n
        ''',
    )

    category = filters.CharFilter(
        field_name="category",
        method="filter_category",
        label="category",
    )

    def check_client(self, request):
        client = self.request.query_params.get('client',None)
        if client is None:
            raise serializers.ValidationError("Client is required")
        return client

    def filter_client_product(self, queryset, name, value):
        return Product.objects.filter(client=value)
    
    def filter_product_choice(self, queryset, name, choice):
        client_q = self.check_client(self.request)
        client = Client.objects.filter(id=client_q).first()
        if choice=="1":
          # return  client.get_top_rated_products
          pass
        if choice=="2":
          return  Product.objects.filter(client=client, is_today_special=True)
        return Product.objects.none()
    def filter_category(self, queryset, name, value):
        client = self.check_client(self.request)
        return Product.objects.filter(client=client,category=value)