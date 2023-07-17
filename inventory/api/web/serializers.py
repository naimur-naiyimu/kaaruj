from inventory.models import *
from rest_framework import serializers
from ...models import *
from coreapp.api.serializers import DocumentSerializer



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','slug', 'main_category','sub_main_category',]


    
class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attributes
        fields = '__all__'
    
class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_details = AttributeSerializer(source='attribute', read_only=True)
    class Meta:
        model = AttributeValue
        fields = '__all__'
    
class VariantSerializer(serializers.ModelSerializer):
    attribute_value_details = AttributeValueSerializer(source='attribute_value', read_only=True,many=True)

    class Meta:
        model = Variant
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    variant_details = VariantSerializer(source='variant', read_only=True,many=True)
    tag_details = TagSerializer(source='tags', read_only=True,many=True)
    category_details = CategorySerializer(source='category', read_only=True,many=True)
    thumb_url = serializers.ReadOnlyField(source='get_thumb_url')
    discount_type_text = serializers.ReadOnlyField(source='get_discount_type')
    offer_price = serializers.ReadOnlyField(source='get_offer_price')
    discount = serializers.ReadOnlyField(source='get_discount')
    is_in_wishlist = serializers.SerializerMethodField()
    feature_image_details = DocumentSerializer(source='feature_images', read_only=True,many=True)

    class Meta:
        model = Products
        fields = '__all__'

    def get_is_in_wishlist(self, obj):
        request = self.context.get('request', None)
        from promotions.models import Wishlist
        if request:
            user = request.user
            if user.is_authenticated:
                return Wishlist.objects.filter(user=user,product=obj).exists()
            else:
                return False
        return False
class ProductListSerializer(serializers.ModelSerializer):
    thumb_url = serializers.ReadOnlyField(source='get_thumb_url')
    discount_type = serializers.ReadOnlyField(source='get_discount_type')
    discount_type_text = serializers.ReadOnlyField(source='get_discount_type_text')
    offer_price = serializers.ReadOnlyField(source='get_offer_price')
    discount = serializers.ReadOnlyField(source='get_discount')
    is_in_wishlist = serializers.SerializerMethodField()
    thumb_url = serializers.ReadOnlyField(source='get_thumb_url')
    variant_details = VariantSerializer(source='variant', read_only=True,many=True)
    
    class Meta:
        model = Products
        fields = ['name','slug','description','thumb_url','variant_details','price','stock','id','discount_type_text','discount_type','offer_price','discount','is_in_wishlist']
    
    def get_is_in_wishlist(self, obj):
        request = self.context.get('request', None)
        from promotions.models import Wishlist
        if request:
            user = request.user
            if user.is_authenticated:
                return Wishlist.objects.filter(user=user,product=obj).exists()
            else:
                return False
        return False
    
class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        exclude = ['created_at','updated_at','attribute']
    

class AttributeSerializer(serializers.ModelSerializer):
    values = AttributeValueSerializer(source='get_values', read_only=True,many=True)
    # values = serializers.ListField(child=serializers.CharField(),source='get_values')
    class Meta:
        model = Attributes
        exclude = ['created_at','updated_at']
        
        
        

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        exclude = ['created_at','updated_at']