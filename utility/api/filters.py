
from django_filters import rest_framework as filters
from ..models import *
from .. import constants
class PageFilter(filters.FilterSet):
    page_type = filters.ChoiceFilter(
        field_name="page_type",
        choices=constants.PageType.choices,
        label = '  '.join([f"{choice[1]} ({choice[0]})" for choice in constants.PageType.choices]),
        method="filter_type",
    )
    
    def filter_type(self, queryset, name, value):
        return Page.objects.filter(page_type=value, is_active=True)