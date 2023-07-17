from fileinput import filename
import json
import traceback
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.signals import user_logged_in
from utility.utils.notification_utils import createNotifications
from sales.helpers import save_pdf, sendPdfEmail
from sales.models import Invoice, Invoice_Products
from inventory.models import Variant, Products, Customer
from django.db.models import Q
from django.db.models.query import QuerySet
from coreapp.models import User
import time
from django.db.models.signals import pre_save
from userapp.models import Notifications
from rest_framework.serializers import ValidationError
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import *
from sales.api.inventory.serializers import InvoiceSerializer
import datetime

def print_log(header,err):
    import logging
    logger = logging.getLogger('django')
    logger.error(header)
    logger.error(err)






def CreateInvoice(sender, instance, created, *args, **kwargs):
    if created:
        data = {}
        data['created_for'] = instance.user.id
        data['source'] = 0
        data['invoice_date'] = datetime.date.today()
        data['bill_to'] = instance.user.first_name + " " + instance.user.last_name
        data['to_mobile'] = instance.shipping_mobile
        data['to_email'] = instance.shipping_email
        data['to_address'] = instance.shipping_street_address
        data['to_zip_code'] = instance.shipping_postcode_zip
        data['to_city'] = instance.shipping_town_city
        data['delivery_charge_type'] = instance.delivery_charge_type
        data['to_division'] = instance.shipping_town_city
        data['to_district'] = instance.shipping_district
        data['to_country'] = instance.shipping_state_county
        data['delivery_type'] = 0
        data['delivery_charge'] = 150
        data['payment_type'] = instance.payment_type
        data['sub_total'] = instance.sub_total
        data['total_due'] = instance.total_due
        data['total_paid'] = instance.total_paid
        data['total_amount'] = instance.total_amount
        data['total_discount'] = instance.total_discount
        data['discount_type'] = 0
        data['send_pdf'] = False
        data['delivery_status'] = 3
        data['payment_status'] = 1
        data['invoice_products'] = []
        for item in instance.cart.item.all():
            invoice_products = {}
            invoice_products['quantity'] = item.quantity
            invoice_products['total'] = item.get_subtotal()
            invoice_products['product_name'] = item.product.name
            invoice_products['variant_name'] = item.variant.name
            invoice_products['product'] = item.product.id
            invoice_products['variant'] = item.variant.id
            data['invoice_products'].append(invoice_products)

        invoice_serializer = InvoiceSerializer(data=data)
        if invoice_serializer.is_valid():
            invoice_serializer.save()
        else:
            print_log("Invoice Create Error",invoice_serializer.errors)

post_save.connect(CreateInvoice, sender=Checkout)