from rest_framework.pagination import LimitOffsetPagination
from django.utils.translation import gettext_lazy as _
from functools import wraps
from django.db.models import QuerySet
from rest_framework.response import Response

class LargeResultsSetPagination(LimitOffsetPagination):
    default_limit = 300
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = None


def paginate(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        queryset = func(self, *args, **kwargs)
        assert isinstance(queryset, (list, QuerySet)), "apply_pagination expects a List or a QuerySet"

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    return inner