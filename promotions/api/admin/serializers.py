from inventory.models import *
from rest_framework import serializers
from ...models import *
from inventory.api.inventory.serializers import ProductListSerializer
from coreapp.api.serializers import DocumentSerializer
class OfferSerializer(serializers.ModelSerializer):
    product_details = ProductListSerializer(read_only=True,source='product',many=True)
    banner_url = serializers.ReadOnlyField(source='get_banner_url')
    class Meta:
        model = Offer
        fields = '__all__'



class ReviewSerializer(serializers.ModelSerializer):
    product_details = ProductListSerializer(read_only=True,source='product')
    photos_details = DocumentSerializer(read_only=True,source='photos',many=True)
    reviewed_by_name = serializers.ReadOnlyField(source='reviewed_by.get_full_name')

    class Meta:
        model = Review
        fields = '__all__'
