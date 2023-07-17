from django.db import models
from coreapp.base import BaseModel
from coreapp.models import User
from utility.utils import model_utils
from . import constants
from sales import constants as sales_constants


class CartItem(BaseModel):
    product = models.ForeignKey("inventory.Products", on_delete=models.CASCADE)
    variant = models.ForeignKey("inventory.Variant", on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def get_subtotal(self):
        return self.product.price * self.quantity


class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(CartItem)
    is_paid = models.BooleanField(default=False)

    def get_total(self):
        return sum(item.get_subtotal() for item in self.item.all())

    def get_product_count(self):
        return sum(item.quantity for item in self.item.all())
    
    def get_product_names(self):
        names = ""
        for item in self.item.all():
            names += item.product.name + ", "
        return names[:-2]
    def get_product_categories(self):

        return "Home Decor / In Style"


class Coupon(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    max_usage = models.PositiveIntegerField(default=3)
    start = models.DateField()
    end = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.client_id = model_utils.get_code(Coupon)
        return super(Coupon, self).save(*args, **kwargs)
  


class BillingInfo(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=20,blank=True)
    company_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    delivery_charge_type = models.SmallIntegerField(choices=sales_constants.deliveryChargeChoices.choices)
    street_address = models.CharField(max_length=255)
    town_city = models.CharField(max_length=255)
    state_county = models.CharField(max_length=255)
    postcode_zip = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    create_account = models.BooleanField(default=False)
    ship_to_different_address = models.BooleanField(default=False)
    shipping_first_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_last_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_company_name = models.CharField(max_length=255, blank=True, null=True)
    shipping_country = models.CharField(max_length=255, blank=True, null=True)
    shipping_district = models.CharField(max_length=255, blank=True, null=True)
    shipping_street_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_town_city = models.CharField(max_length=255, blank=True, null=True)
    shipping_state_county = models.CharField(max_length=255, blank=True, null=True)
    shipping_postcode_zip = models.CharField(max_length=20, blank=True, null=True)
    shipping_mobile = models.CharField(max_length=20, blank=True, null=True)
    shipping_email = models.EmailField(blank=True, null=True)
    order_notes = models.TextField(blank=True, null=True)

    @property
    def get_full_name(self):
        return f"{self.shipping_first_name} {self.shipping_last_name}"

    def save(self, *args, **kwargs):
        if not self.ship_to_different_address:
            self.shipping_first_name = self.first_name
            self.shipping_last_name = self.last_name
            self.shipping_company_name = self.company_name
            self.shipping_country = self.country
            self.shipping_district = self.district
            self.shipping_street_address = self.street_address
            self.shipping_town_city = self.town_city
            self.shipping_state_county = self.state_county
            self.shipping_postcode_zip = self.postcode_zip
            self.shipping_mobile = self.mobile
            self.shipping_email = self.email
        super().save(*args, **kwargs)


class Checkout(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    tran_id = models.CharField(max_length=255, null=True, blank=True)
    coupon = models.ForeignKey(Coupon,null=True,blank=True, on_delete=models.CASCADE)
    billing_info = models.ForeignKey(BillingInfo, on_delete=models.CASCADE)
    payment_type =  models.SmallIntegerField(choices=constants.PaymentType.choices)
    shipping_type =  models.SmallIntegerField(choices=constants.ShippingType.choices)
    sub_total = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)
    total_due = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)
    total_paid = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)
    total_amount = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)
    total_discount = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)

    def __str__(self):
        return self.user.email