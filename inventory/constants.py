from django.db import models
from django.utils.translation import gettext_lazy as _


# Gender  Options
class MainCategoryChoices(models.IntegerChoices):
    HOME_DECOR = 0, _("Home Decor")
    IN_STYLE = 1, _("In Style")

class SubMainCategoryChoices(models.IntegerChoices):
    FOR_DINING = 0, _("For Dining")
    FOR_LIVING = 1, _("For Living")
    CASUAL_WEAR = 2, _("Casual Wear")
    PARTY_WEAR = 3, _("Party Wear")
    EXCLUSIVE_WEAR = 4, _("Exclusive Wear")
    FOOT_WEAR = 5, _("Foot Wear")
    FOR_COUPLES = 6, _("For Couples")
    KIDS_ZONE = 7, _("Kids Zone")

class ProductSortChoices(models.IntegerChoices):
    POPULARITY = 0, _("Popularity")
    RATING = 1, _("Rating")
    LATEST = 2, _("Latest")
    PRICE_LOW_TO_HIGH = 3, _("Price Low to High")
    PRICE_HIGH_TO_LOW = 4, _("Price High to Low")


class CategoryType(models.IntegerChoices):
    MAINCATEGORY = 0, _("Main Category")
    SUBMAINCATEGORY = 1, _("Sub Main Category")
    OTHERCATEGORY = 2, _("Other Category")