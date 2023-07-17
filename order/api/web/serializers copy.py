from inventory.models import *
from rest_framework import serializers
from ...models import *
from coreapp.api.serializers import SignupSerializer

class BillingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingInfo
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
class CartSerializer(serializers.ModelSerializer):
    item = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['user']


class CartSerializerForCreateInCheckout(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CheckoutSerializerForShow(serializers.ModelSerializer):
    billing_info_details = BillingInfoSerializer()
    cart_details = CartSerializer()

    class Meta:
        model = Checkout
        fields = '__all__'
        read_only_fields = ['billing_info']


class CheckoutSerializer(serializers.ModelSerializer):
    billing_info = BillingInfoSerializer()
    cart = CartSerializer()

    class Meta:
        model = Checkout
        fields = '__all__'
        read_only_fields = ['billing_info', 'user']

    def create_user(self,billing_data):
        signup_data = {
            'first_name': billing_data['first_name'],
            'last_name': billing_data['last_name'],
            'email': billing_data['email'],
            'mobile': billing_data['mobile'],
            'password': billing_data['password'],
            'confirm_password': billing_data['password'],
            # 'country': billing_data['country'],
        }
        user_serializer = SignupSerializer(data=signup_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        return user
    
    def create_billing_info(self, billing_data):
        billing_info_serializer = BillingInfoSerializer(data=billing_data)
        billing_info_serializer.is_valid(raise_exception=True)
        billing_info = billing_info_serializer.save()
        return billing_info
    
    def create_cart_items(self, cart_items_data):
        print("cart_items_data",cart_items_data)
        data = []
        for items in cart_items_data:
            items['product'] = items['product'].id
            items['variant'] = items['variant'].id
            cart_items_serializer = CartItemSerializer(data=items)
            cart_items_serializer.is_valid(raise_exception=True)
            cart_items = cart_items_serializer.save()
            data.append(cart_items.id)
        return data

    def create_cart(self, validated_data):
        cart_data = validated_data.pop('cart')
        cart_data['item'] = self.create_cart_items(cart_data['item'])
        cart_data['user'] = validated_data['user'].id
        print("cart_data_2323", cart_data)
        cart_serializer = CartSerializerForCreateInCheckout(data=cart_data)
        cart_serializer.is_valid(raise_exception=True)
        cart = cart_serializer.save()
        return cart

    def create(self, validated_data):
        request = self.context.get('request')
        billing_info_data = validated_data.pop('billing_info')

        validated_data['billing_info'] = self.create_billing_info(billing_info_data)
        create_account = billing_info_data.pop('create_account')
        if create_account:
            current_user = self.create_user(billing_info_data)
        else:
            current_user = request.user
        validated_data['user'] = current_user
        print("validated_data_user", validated_data['user'])
        validated_data['cart'] = self.create_cart(validated_data)
        print("validated_data", validated_data)
        checkout = super().create(validated_data)
        return checkout


class VerifyCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['code']