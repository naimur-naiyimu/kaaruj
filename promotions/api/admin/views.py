
from . import serializers
from ...models import *
from coreapp.helper import *

class OfferAPI(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = serializers.OfferSerializer
    permission_classes = [IsAdminUser,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product',]
    search_fields = ['product__name','name','description']
class ReviewAPI(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAdminUser,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product','reviewed_by','star']
    search_fields = ['product__name','descriptions']

