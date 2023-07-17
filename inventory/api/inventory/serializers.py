from ...models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from coreapp.api.serializers import DocumentSerializer
class CategorySerializer(serializers.ModelSerializer):
    
    subcategories = serializers.SerializerMethodField()
    thumb_url = serializers.ReadOnlyField(source='get_thumb_url')
    # parent_name = serializers.ReadOnlyField(source='parent.name', allow_null=True)
    # tree = serializers.ReadOnlyField(source="category_tree_exclude_current")
    products = serializers.ReadOnlyField(source="count_products")
    tree = serializers.ReadOnlyField(source="get_string_tree")

    class Meta:
        model = Category
        # fields = ['id', 'name','level', 'subcategories']
        fields = '__all__'
        read_only_fields = ['slug',]

    def get_subcategories(self, obj):
        subcategories = Category.objects.filter(parent=obj)
        serializer = CategorySerializer(subcategories, many=True)
        return serializer.data
    


    

        
    
class AttributeValueSerializer(serializers.ModelSerializer):
    # attribute_details = AttributeSerializer(source='attribute', read_only=True)]
    class Meta:
        model = AttributeValue
        fields = '__all__'
    
class VariantSerializer(serializers.ModelSerializer):
    # attribute_value_details = AttributeValueSerializer(source='attribute_value', read_only=True,many=True)
    attribute_value = AttributeValueSerializer(many=True)
    class Meta:
        model = Variant
        fields = '__all__'
    


    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

class CategorySerializerForProducts(ModelSerializer):
    class Meta:
        model = Category
        # fields = ['id', 'name']
        fields = "__all__"
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        

class ProductSerializerForInvoice(ModelSerializer):
    variants = VariantSerializer(source='variant', read_only=True,many=True)
    discount = serializers.ReadOnlyField(source='get_discount')
    thumb_url = serializers.ReadOnlyField(source='thumb.get_url')
    class Meta:
        model = Products
        fields = ['id','name','thumb','sku','variants','discount','price','stock','thumb_url',]
    



# class ProductCreateUpdateUtils():
#     def validate(self, data):
#         sku = data.get('sku')
#         if self.instance is not None:
#             existing_product = Products.objects.filter(sku=sku).exclude(id=self.instance.id).first()
#         else:
#             existing_product = Products.objects.filter(sku=sku).first()
#         print("existing_product12323434",existing_product)
#         # if existing_product:
#         #     raise serializers.ValidationError('A product with this SKU already exists.')
#         return data

class ProductCreateUpdateUtils():
    # ...

    def create_attributes_values(self, data):
        data = data.get('attribute_value')
        attribute_values = []
        for attribute_value_data in data:
            attribute_id = attribute_value_data.pop('attribute')
            value = attribute_value_data.pop('value')
            try:
                attribute_id = attribute_id.id
            except:
                attribute_id = attribute_id
            attribute = Attributes.objects.get(id=attribute_id)  # Retrieve the attribute instance
            attribute_value_queryset = AttributeValue.objects.filter(attribute=attribute, value=value, **attribute_value_data)
            if attribute_value_queryset.exists():
                attribute_value = attribute_value_queryset.first()
            else:
                attribute_value = AttributeValue.objects.create(attribute=attribute, value=value, **attribute_value_data)
            attribute_values.append(attribute_value)
        return attribute_values

    # ...
    def update_attribute_values(self, data):
        attribute_values_list = []
        attribute_values = data
        for attrs in attribute_values:
            att_val_serializer = AttributeValueSerializer(data=attrs)
            if att_val_serializer.is_valid():
                att_val_serializer.save()
                attribute_values_list.append(att_val_serializer.data.get('id'))
        return attribute_values_list
        # return attribute_values
    def create_variants(self, data):
        variants = []
        for variant_data in data:
            attribute_values = self.create_attributes_values(variant_data)
            variant_data.pop('attribute_value') #dont need this here
            variant = Variant.objects.create(**variant_data)
            for attribute_value in attribute_values:
                variant.attribute_value.add(attribute_value.id)     
            variants.append(variant)
        return variants
    

    def update_variants(self, variant_data, instance):
        variants = []
        for data in variant_data:
            attribute_values = self.update_attribute_values(data.get('attribute_value'))
            variant = Variant.objects.filter(id=data.get('id')).first()
            variant.attribute_value.set(attribute_values)
            variant.name = data.get('name')
            variant.price = data.get('price')
            variant.stock = data.get('stock')
            variant.save()
            variants.append(variant.id)
        return variants

        # return attribute_values_list

    
    def create_or_get_tags(self, data):
        tags = []
        for tag_data in data:
            tag_queryset = Tags.objects.filter(name=tag_data['name'])
            if tag_queryset.exists():
                tag = tag_queryset.first()
            else:
                tag = Tags.objects.create(**tag_data)
            tags.append(tag)
        return tags




class ProductSerializer(serializers.ModelSerializer,ProductCreateUpdateUtils):
    # variant_details = VariantSerializer(source='variant', read_only=True,many=True)
    tag_details = TagSerializer(source='tags', read_only=True,many=True)
    category_details = CategorySerializer(source='category', read_only=True,many=True)
    thumb_url = serializers.ReadOnlyField(source='get_thumb_url')
    variant =VariantSerializer(many=True)
    tags = TagSerializer(many=True)
    rating = serializers.ReadOnlyField(source = "get_rating")
    discount = serializers.ReadOnlyField(source='get_discount')

    feature_images_details = DocumentSerializer(source='feature_images', read_only=True,many=True)
    variants_json = serializers.SerializerMethodField()
    variant_json_previous = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ['slug','barcode','qrcode']

    def get_variant_json_previous(self, obj):
        return obj.variants_json

    def get_variants_json(self, obj):
        variants = obj.variant.all()
        variant_json = {
            'mainState': {},
            'AttributesInputValue': {}
        }

        for variant in variants:
            attribute_values = variant.attribute_value.all()
            color_values = []

            for attribute_value in attribute_values:
                color_values.append(attribute_value.value)

            variant_data = {
                'variant_stock': str(variant.stock),
                'variant_name': variant.name,
                'attribute_value': [
                    {
                        'attribute': 'Color',
                        'value': color_value
                    } for color_value in color_values
                ],
                'variant_price': str(variant.price)
            }

            for color_value in color_values:
                if color_value not in variant_json['mainState']:
                    variant_json['mainState'][color_value] = []
                variant_json['mainState'][color_value].append(variant.name)
                variant_json['AttributesInputValue'][variant.name] = variant_data
            variant_json['mainState']={}
            for variant in obj.variant.all():
                for attribute in variant.attribute_value.all():
                    attribute_name = attribute.attribute.name
                    if attribute_name not in variant_json['mainState']:
                        variant_json['mainState'][attribute_name] = []
                    if attribute.value not in variant_json['mainState'][attribute_name]:
                        variant_json['mainState'][attribute_name].append(attribute.value)


        return variant_json
    # def validate(self, data):
    #     # return data
    #     sku = data.get('sku')
    #     if self.instance is not None:
    #         existing_product = Products.objects.filter(sku=sku).exclude(id=self.instance.id).first()
    #     else:
    #         existing_product = Products.objects.filter(sku=sku).first()
    #     if existing_product:
    #         print("existing_product12323434",existing_product)
    #         print("existing_product12323434",existing_product.id)
    #         print("existing_product12323434",self.instance)
    #         raise serializers.ValidationError('A product with this SKU already exists.')
    #     return data




    def create(self, validated_data):
        print("Create Method Called --- Check23232")
        variant_data = self.create_variants(validated_data.pop('variant'))
        tags_data = self.create_or_get_tags(validated_data.pop('tags'))
        categories = validated_data.pop('category')
        feature_images = validated_data.pop('feature_images',[])

        product = Products.objects.create(**validated_data)

        product.variant.set(variant_data)
        product.category.set(categories)
        product.tags.set(tags_data)
        product.feature_images.set(feature_images) 

        return product 

  
        
class ProductSerializer_Update(serializers.ModelSerializer,ProductCreateUpdateUtils):
    variant_update_info = serializers.ListField(child=serializers.DictField(),write_only=True)
    # variant_details = VariantSerializer(source='variant', read_only=True,many=True)
    variant_details = VariantSerializer(source='variant', read_only=True,many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ['slug','barcode','qrcode']

    def update(self, instance, validated_data):
        variant_data = validated_data.get('variant_update_info') 
        if variant_data:
            for variant in variant_data:
                variant_id = variant.get('id',None)
                if variant_id is None:
                    variant_no_id = self.create_variants([variant])
                    instance.variant.add(variant_no_id[0])

                else:
                    variant_with_id = self.update_variants([variant],instance)
                    instance.variant.add(variant_with_id[0])

        tags = validated_data.pop('tags',None)
        if tags:
            tags_data = self.create_or_get_tags(tags)
            instance.tags.set(tags_data)
        instance.save()
        instance = super(ProductSerializer_Update,self).update(instance, validated_data)
        return instance

class ProductListSerializer(serializers.ModelSerializer):
    thumb_url = serializers.ReadOnlyField(source='get_thumb_url')
    discount = serializers.ReadOnlyField(source='get_discount')
    category_details = CategorySerializer(source='category', read_only=True,many=True)
    variant_details = VariantSerializer(source='variant', read_only=True,many=True)
    # thumb_resized = serializers.ReadOnlyField(source="get_thumb_resized_url")


    class Meta:
        model = Products
        fields = ['id', 'name', 'category','thumb_resized','variant_details','category_details','discount', 'stock', 'thumb_url', 'stock', 'slug', 'sku', 'is_active', "updated_at", ]
    




class AttributeSerializer(ModelSerializer):
    class Meta:

        model = Attributes
        fields = "__all__"


class CustomerSerializer(ModelSerializer):
    total_purchase = serializers.ReadOnlyField(source="total")
    count = serializers.ReadOnlyField(source="invoice_count_method")
    class Meta:

        model = Customer
        fields = "__all__"
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }
        

class CustomerSerializerForInvoice(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','name','email','address','mobile']
        # fields = ["id", "name", "email", "mobile", "total_purchase", "status"]


class BulkProductSerializer(serializers.Serializer):
    file = serializers.FileField()