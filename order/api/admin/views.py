
from . import serializers
from ...models import *
from coreapp.models import User
from coreapp.helper import *


class CouponAPI(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = serializers.CouponSerializer
    permission_classes = [IsAdminUser,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['code','is_active']
    search_fields = ['code','discount_amount']