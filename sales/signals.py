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
import asyncio
import threading
from rest_framework.serializers import ValidationError
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
def print_log(header,err):
    import logging
    logger = logging.getLogger('django')
    logger.error(header)
    logger.error(err)


def createCustomer(sender, instance, *args, **kwargs):
    try:
        mobile = instance.to_mobile
        address = instance.to_address

        findCustomer = Customer.objects.filter(mobile=mobile).first()

        if findCustomer == None:
            customer = Customer.objects.create(name=instance.bill_to, mobile=mobile,
                                            email=instance.to_email, status=True,
                                            to_address = instance.to_address,
                                            to_address2 = instance.to_address2,
                                            to_zip_code = instance.to_zip_code,
                                            to_city = instance.to_city,
                                            to_division = instance.to_division,
                                            to_district = instance.to_district,
                                            to_country = instance.to_country,
                                            )
        else:  # user exists ,then have to update phone,address
            # findCustomer.total_purchase = total
            if findCustomer.to_address != address:
                findCustomer.to_address = address
                findCustomer.save()
            print("---------Customer updated from signal---------")
    except Exception as e:
        traceback.print_exc()
        print_log("---------Customer create/update issue---------",str(e))




def ReduceVariantStock(sender, instance, created, *args, **kwargs):
    print("---------Stock update from signal---------")
    if created:
        try:
            product = instance.product
            variant = instance.variant
            quantity = instance.quantity

            # Check if variant stock is available

            if variant:
                if variant.stock >= quantity:
                    variant.stock -= quantity
                    variant.save()
                else:
                    raise ValidationError(f"Insufficient stock for variant: {variant}")

            # Check if product stock is available
            if product:
                if product.stock >= quantity:
                    product.stock -= quantity
                    product.save()
                else:
                    raise ValidationError(f"Insufficient stock for product: {product}")

        except Exception as e:
            traceback.print_exc()
            print_log("---------Stock update issue---------",str(e))



def send_stock_notifications(sender, instance, created, *args, **kwargs):
    try:
        name = instance.name
        stock = instance.stock
        if stock < 10:
            title = "Low Inventory"
            info = f'''<span class="fw-bold">{name}'s</span> stock is too <span class="fw-bold">low</span>! Current stock : {stock} </span>'''
            notification = Notifications.objects.create(title=title, info=info)

    except Exception as e:
        traceback.print_exc()
        print_log("---------Stock notification issue---------",str(e))





def SavePdfAndSendMail(sender, instance, created, **kwargs):
    if  instance.send_pdf:
        t = threading.Thread(target=save_send_pdf_async_func, args=(instance,))
        t.start()



        
def save_send_pdf_async_func(instance):
    try:
        print("sendPdf", instance.send_pdf)
        params = {}
        params['qr_code'] = instance.qr_code
        params['number'] = instance.number
        params['invoice_date'] = instance.invoice_date
        params['bill_from'] = instance.bill_from
        params['bill_to'] = instance.bill_to
        params['from_email'] = instance.from_email
        params['to_email'] = instance.to_email
        params['from_mobile'] = instance.from_mobile
        params['to_mobile'] = instance.to_mobile
        params['from_address'] = instance.from_address
        params['to_address'] = instance.to_address
        if instance.delivery_type == 0:
            params['delivery_type'] = "Regular"
        else:
            params['delivery_type'] = "Urgent"

        params['delivery_charge'] = instance.delivery_charge
        params['delivery_charge_type'] = instance.delivery_charge_type


        params['payment_type'] = ["COD", "Card", "Bank", "Bkash"][instance.payment_type]
        params['delivery_status'] = instance.delivery_status
        params['total_due'] = instance.total_due
        params['total_paid'] = instance.total_paid
        params['total_amount'] = instance.total_amount
        params['total_discount'] = instance.total_discount
        if instance.payment_status == 0:
            params['payment_status'] = "Paid"
        if instance.payment_status == 1:
            params['payment_status'] = "UnPaid"
        if instance.payment_status == 2:
            params['payment_status'] = "Due"
        params['notes'] = instance.notes
        params['total_due'] = instance.total_due
        params['total_paid'] = instance.total_paid
        params['total_amount'] = instance.total_amount
        params['total_discount'] = instance.total_discount
        params['invoice_view_json'] = instance.invoice_view_json
        params['header_image_url'] = "https://inventory.clients.devsstream.com/media/default/KAARUJ_PDF_Header.png"
        params['sub_total'] = instance.sub_total
        params['invoice_products'] = instance.get_invoice_products()
        print("inv_prods", params['invoice_products'])
        filepath, status = save_pdf(params)
        subject = f'#{instance.number} from {instance.bill_from}'
        message = f"Thanks {instance.bill_to},For choosing us"
        # to_mail = ["kaarujbangladesh@gmail.com"]
        to_mail = [instance.to_email]
        from_mail = instance.from_email
        sendPdfEmail(subject, message,  from_mail, to_mail, filepath)
    except Exception as e:
        traceback.print_exc()
        print_log("---------PDF create issue---------",str(e))
    current_thread = threading.current_thread()
    for thread in threading.enumerate():
        if thread == current_thread:
            continue
        thread.join()

def UpdateProductOnReturn(sender, instance, created, **kwargs):
    print("---------Product update from signal-1234343--------")
    try:
        if not created and instance.delivery_status==0 and instance.is_stock_updated_after_return==False:
            inv_products = instance.get_invoice_products()
            for inv_product in inv_products:
                product = Products.objects.get(id=inv_product.product.id)
                product.stock += inv_product.quantity
                product.save()
                variant = Variant.objects.get(id=inv_product.variant.id)
                variant.stock += inv_product.quantity
                variant.save()
            instance.is_stock_updated_after_return = True
            instance.save()
    except Exception as e:
        print_log("---------custom invoice update issue---------",str(e))

def createNotificationsForInvoice(sender, created, instance, *args, **kwargs):
    if created:
        created_by = instance.created_by if instance.created_by else "Customer(From Wesite)"
        title = f"Invoice Created (#{instance.number})"
        notification_info = " Generated Invoice for"
        created_by = instance.created_by
        createNotifications(title=title, notification_info=notification_info,
                            created_by=instance.created_by, created_who=instance.bill_to)
        


post_save.connect(createNotificationsForInvoice, sender=Invoice)
post_save.connect(send_stock_notifications, sender=Products)
post_save.connect(SavePdfAndSendMail, sender=Invoice)
post_save.connect(createCustomer, sender=Invoice)
post_save.connect(UpdateProductOnReturn, sender=Invoice)
post_save.connect(ReduceVariantStock, sender=Invoice_Products)