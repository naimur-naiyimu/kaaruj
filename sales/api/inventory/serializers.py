from ...models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class InvoiceProductSerializer(ModelSerializer):
    thumb = serializers.ReadOnlyField(source='product.get_thumb_url')
    class Meta:
        model = Invoice_Products
        fields = '__all__'

class VariantSerializerInvoice(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields='__all__'

class InvoiceProductSerializerInvoice(serializers.ModelSerializer):
    variant_details = VariantSerializerInvoice(read_only=True,source= 'variant')
    product_thumb = serializers.ReadOnlyField(source='product.get_thumb_url')
    product_name = serializers.SerializerMethodField()
    product_price = serializers.ReadOnlyField(source='product.price')
    class Meta:
        model = Invoice_Products
        fields = ['id', 'variant', 'quantity', 'total','product_name','product_price','product_thumb','variant_details']
    def get_product_name(self, instance):
        return instance.product.name if instance.product else instance.product_name
    

class InvoiceListSerializer(serializers.ModelSerializer):
    prepared_by = serializers.ReadOnlyField(source='created_by.get_full_name')
    class Meta:
        model =  Invoice
        fields = ['id','slug','number','source','prepared_by','is_custom','delivery_type','delivery_status','payment_status','payment_type','payment_status','total_amount','invoice_date']

  
class InvoiceSerializer(ModelSerializer):
    invoice_products = InvoiceProductSerializer(many=True)
    invoice_products_formatted = serializers.SerializerMethodField()
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['slug','number','qr_code','qr_code_text']

    def create(self, validated_data):
        invoice_products = validated_data.pop('invoice_products')
        invoice = Invoice.objects.create(**validated_data)
        for invoice_product in invoice_products:
            created_invoice_product = Invoice_Products.objects.create(invoice=invoice, **invoice_product)
            invoice.invoice_products.add(created_invoice_product)
        return invoice

    def get_invoice_products_formatted(self, instance):       
        invoice_products = {}
        for invoice_product in instance.invoice_products.all().order_by('created_at'):
            product_name = invoice_product.product.name if invoice_product.product else invoice_product.product_name
            if product_name not in invoice_products:
                invoice_products[product_name] = []
            invoice_product_data = InvoiceProductSerializerInvoice(invoice_product).data
            invoice_products[product_name].append(invoice_product_data)
        return invoice_products
     
class InvoiceSerializer_Update(ModelSerializer):
    invoice_products_details = serializers.ListField(child=serializers.DictField(),write_only=True)
    invoice_products = InvoiceProductSerializer(many=True,read_only=True)
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['slug','number','qr_code','qr_code_text']

    def update(self,instance, validated_data):
        invoice_products = validated_data.pop('invoice_products_details',[])
        for invoice_product in invoice_products:
            invoice_product_id = invoice_product.get('id')
            if invoice_product_id:
                inv_prod_instance =Invoice_Products.objects.get(id=invoice_product_id)
                serializer_inv_prod = InvoiceProductSerializer(data=invoice_product,instance=inv_prod_instance,partial=True)
                if serializer_inv_prod.is_valid():
                    serializer_inv_prod.save()
                
            else:
                try:
                    invoice_product['product'] = Products.objects.get(id=invoice_product.get('product'))
                    invoice_product['variant'] = Variant.objects.get(id=invoice_product.get('variant'))
                except Exception as e:
                    print(str(e))
                created_invoice_product = Invoice_Products.objects.create( **invoice_product)
                instance.invoice_products.add(created_invoice_product)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class All_InvoiceSerializer(serializers.ModelSerializer):
    prepared_by = serializers.ReadOnlyField(source='created_by.get_full_name')

    class Meta:
        model =  Invoice
        fields = "__all__"
