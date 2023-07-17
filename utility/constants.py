from django.db import models
from django.utils.translation import gettext_lazy as _


# Page  Options
class PageType(models.IntegerChoices):
    HOMEPAGE = 1, _("Homepage")
    HOME_DECOR = 2, _("Home Decor")
    IN_STYLE = 3, _("In Style")

# Page  Options
class ShowType(models.IntegerChoices):
    VIDEO = 0, _("Video")
    SLIDER = 1, _("Slider")


# Payment Status
class PaymentStatus(models.IntegerChoices):
    PENDING = 0, _("Pending")
    SUCCESS = 1, _("Success")
    CANCELLED = 2, _("Cancelled")
    FAILED = 3, _("Failed")


# Payment Method
class PaymentMethod(models.IntegerChoices):
    PAYPAL = 0, _("Paypal")
    BILLPLZ = 1, _("BillPlz")
    CASH = 2, _("Cash")
class InquiryType(models.IntegerChoices):
    URGENT = 0, _("Urgent")
    NORMAL = 1, _("Normal")
class ContactType(models.IntegerChoices):
    CONTACT = 0, _("Contact Us")
    WORK = 1, _("Work With Us")
