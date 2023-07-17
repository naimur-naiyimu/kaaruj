from django.db import models
from django.utils.translation import gettext_lazy as _


class InvoiceChoices(models.IntegerChoices):
    PAID = 0, _("Paid")
    UNPAID = 1, _("Unpaid")
    DUE = 2, _("Due")

class SourceChoices(models.IntegerChoices):
    WEBSITE = 0, _("Ecommerce Website")
    INVENTORY = 1, _("Inventory")
    ADMIN = 2, _("Admin Panel")

class DiscountChoices(models.IntegerChoices):
    FLAT = 0, _("Flat")
    PERCENTAGE = 1, _("Percentage")


class DeliveryTypeChoices(models.IntegerChoices):
    REGULAR = 0, _("Regular")
    URGENT = 1, _("Urgent")


class deliveryChargeChoices(models.IntegerChoices):
    INSIDE_DHAKA = 0, _("Inside Dhaka : 80/-")
    OUTSIDE_DHAKA = 1, _("Outside Dhaka : 150/-")
    CUSTOM = 2, _("Custom")



class PaymentTypeChoices(models.IntegerChoices):
    COD = 0, _("Cash On Delivery")
    SSLECOMMERZ = 1, _("SSLCOMMERZ")


class DeliveryStatusChoices(models.IntegerChoices):
    RETURNED = 0, _("Returned")
    RECIEVED = 1, _("Recieved")
    DELIVERED = 2, _("Delivered")
    PENDING = 3, _("Pending")
    HOLD = 4, _("Hold")
    DISPATCHED = 5, _("Dispatched")
