from django.db import models
from django.utils.translation import gettext_lazy as _


class OfferType(models.IntegerChoices):
    PERCENTAGE = 0, _("Percentage")
    FLAT = 1, _("Flat")
