from inventory.models import *
from rest_framework import serializers
from ...models import *
from inventory.api.web.serializers import *
class OfferSerializer(serializers.ModelSerializer):
    products_details = ProductListSerializer(many=True, read_only=True,source='product')
    category_details = CategorySerializer(many=True, read_only=True,source='category')
    class Meta:
        model = Offer
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'