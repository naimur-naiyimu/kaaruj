from django.db import models
from django.utils.translation import gettext_lazy as _


# Model  Options
class ModelChoices(models.IntegerChoices):
    PRODUCT = 0, _("Product")
    CATEGORY = 1, _("Category")
    INVOICE = 2, _("Invoice")
    USER = 3, _("User")


