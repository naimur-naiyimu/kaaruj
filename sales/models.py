
from django.db import models
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
# Create your models here.
import random
from django.db.models import Q
import datetime

from coreapp.base import BaseModel
from inventory.models import Variant, Products
from . import constants
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from rest_framework.decorators import action

from utility.utils import filter_utils,model_utils,slug_utils
import string
import json
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

def validate_only_letters_and_spaces(value):
    if not value or not value.replace(" ", "").isalpha():
        raise ValidationError("Only letters and spaces are allowed.")
    
def get_random_string(length):
    letters = string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return int(result_str)



class Invoice_Products(BaseModel):
    product = models.ForeignKey("inventory.Products", blank=True, null=True, on_delete=models.SET_NULL)
    variant = models.ForeignKey("inventory.Variant", blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)
    total = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    variant_name = models.CharField(max_length=100, blank=True, null=True)
    is_custom = models.BooleanField(default=False)
    invoice_date = models.DateField()

    def __init__(self, *args, **kwargs):
        super(Invoice_Products, self).__init__(*args, **kwargs)
        self.prev_quantity = self.quantity

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        if self.product != None:
            return self.product.name
        else:
            return self.product_name

    def save(self, *args, **kwargs):
        if self.product:
            self.product_name = self.product.name
        super().save(*args, **kwargs)

class Invoice(BaseModel):
    number = models.CharField(max_length=50, blank=True, unique=True)
    invoice_products = models.ManyToManyField(Invoice_Products, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/invoice/', blank=True)
    qr_code_text = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    source = models.SmallIntegerField(choices=constants.SourceChoices.choices,default=1)
    invoice_date = models.DateField()
    bill_from = models.CharField(max_length=50,default="KAARUJ")
    bill_to = models.CharField(max_length=50)
    from_mobile = models.CharField(max_length=50,default='+8801980907892')
    to_mobile = models.CharField(max_length=50)
    from_email = models.CharField(max_length=150,default="kaarujbangladesh@gmail.com")
    to_email = models.CharField(max_length=150, blank=True, null=True)
    from_address = models.CharField(max_length=350,default="House 148, Block- B, Road 5, Basundhara R/A, Dhaka, Bangladesh")
    to_address = models.CharField(max_length=350)
    to_address2 = models.CharField(max_length=350, blank=True, null=True)
    to_zip_code = models.CharField(max_length=50, blank=True, null=True)
    to_city = models.CharField(max_length=50, blank=True, null=True)
    to_division = models.CharField(max_length=50, blank=True, null=True)
    to_district = models.CharField(max_length=50, blank=True, null=True)
    to_country = models.CharField(max_length=50, blank=True, null=True)
    delivery_type = models.SmallIntegerField(choices=constants.DeliveryTypeChoices.choices)
    delivery_charge = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)
    delivery_charge_type = models.SmallIntegerField(choices=constants.deliveryChargeChoices.choices)
    payment_type = models.SmallIntegerField(choices=constants.PaymentTypeChoices.choices)
    discount_type = models.SmallIntegerField(choices=constants.DiscountChoices.choices)
    delivery_status = models.SmallIntegerField(choices=constants.DeliveryStatusChoices.choices)
    sub_total = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)
    total_due = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)
    total_paid = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)
    total_amount = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)
    total_discount = models.DecimalField(default=00.00, decimal_places=2, max_digits=10)
    payment_status = models.SmallIntegerField(choices=constants.InvoiceChoices.choices)
    notes = models.TextField(blank=True, null=True)
    product_list_json = models.JSONField(blank=True, null=True)
    invoice_view_json = models.JSONField(blank=True, null=True)
    created_for = models.ForeignKey("coreapp.user", on_delete=models.SET_NULL, blank=True, null=True, related_name="invoice_created_for")
    created_by = models.ForeignKey("coreapp.user", on_delete=models.SET_NULL, blank=True, null=True, related_name="invoice_created_by")
    send_pdf = models.BooleanField()
    card_holder_name = models.CharField(max_length=100, blank=True, null=True, validators=[validate_only_letters_and_spaces])
    card_number = models.IntegerField(max_length=100, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True, validators=[validate_only_letters_and_spaces])
    banK_account_number = models.CharField(max_length=100, blank=True, null=True)
    banK_account_name = models.CharField(max_length=100, blank=True, null=True,validators=[validate_only_letters_and_spaces])
    banK_branch_name = models.CharField(max_length=100, blank=True, null=True)
    bkash_number = models.CharField(max_length=11, blank=True, null=True)
    bkash_trx_number = models.CharField(max_length=11, blank=True, null=True)
    nagad_number = models.CharField(max_length=11, blank=True, null=True)
    nagad_trx_number = models.CharField(max_length=11, blank=True, null=True)
    is_custom = models.BooleanField(default=False)
    is_stock_updated_after_return = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.number


    @property
    def total_amount_with_discount(self):
        import math
        if (self.discount_type == 0):

            return int(self.total_amount) - int(self.total_discount)
        else:
            return int(self.total_amount) - (int(self.total_amount) * (int(self.total_discount) / 100))

    def get_invoice_products(self):
        return self.invoice_products.all()


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        notification= Notification.objects.get()
        notification.invoice += 1
        notification.save()

        if not self.number:
            self.number = model_utils.get_invoice_code(Invoice, prefix="INV")
        if not self.slug:
            self.slug = self.number
            # self.slug = slug_utils.generate_unique_slug(self.number, self)
        if not self.id:
            model_utils.generate_qrcode(self, self.number)

        return super(Invoice, self).save(*args, **kwargs)


@receiver(post_save, sender=Invoice)
def increment_notification_count(sender, instance, created, **kwargs):
    if not created:
        notification, _ = Notification.objects.get_or_create(user=instance.created_by)
        notification.invoice += 1
        notification.save()
        


# class DailyReport(BaseModel):
#     products = models.ForeignKey(Products, on_delete=models.CASCADE,blank=True,null=True)
#     quantity = models.IntegerField()
#     total_amount = models.CharField(max_length=100)
#     product_name = models.CharField(max_length=100, blank=True, null=True)
#     is_custom = models.BooleanField(default=False)

#     class Meta:
#         ordering = ('-created_at',)

#     def __str__(self):
#         return self.created_at.strftime('%d/%m/%Y')




# class DailyReport(BaseModel):

class DailyReport(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField()
    total_amount = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    is_custom = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.created_at.strftime('%d/%m/%Y')

# class DateTest(models.Model):
#     created_at = models.DateTimeField()
#     class Meta:
#         ordering = ('-created_at',)

#     def __str__(self):
#         return  self.created_at.strftime('%d/%m/%Y')


class Notification(models.Model):
    user = models.ForeignKey("coreapp.user", on_delete=models.CASCADE)
    invoice = models.IntegerField(default=0)
    reviews = models.IntegerField(default=0)
    contact_us = models.IntegerField(default=0)
    work_us = models.IntegerField(default=0)
    
    # def __str__(self):
    #     return self.user
