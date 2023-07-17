from django.db import models
from django.utils.translation import gettext_lazy as _


class PaymentType(models.IntegerChoices):
    COD = 0, _("Cash On Delivery")
    CARD = 1, _("Card")
    BANK = 2, _("Bank")
    BKASH = 3, _("Bkash")
    SSLECOMMERZ = 4, _("SSLCOMMERZ")

class ShippingType(models.IntegerChoices):
    HOME  = 0, _("Home Delivery")
    PICKUP = 1, _("Pickup Points")
    OTHERS = 2, _("Others")
class CheckoutStatus(models.IntegerChoices):
    PENDING  = 0, _("Pending")
    SUCCESS = 1, _("Success")
    FAILED = 2, _("Failed")
