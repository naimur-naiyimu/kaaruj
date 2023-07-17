
from . import serializers
from ...models import *
from coreapp.helper import *
from rest_framework.permissions import IsAuthenticated, AllowAny

class OfferAPI(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = serializers.OfferSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get']

class ReviewAPI(viewsets.ModelViewSet):
    queryset = Review.objects.filter(is_active=True)
    serializer_class = serializers.ReviewSerializer
    permission_classes = [AllowAny,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['product',]
    http_method_names = ['get','post']
    
    def get_permissions(self):
        if self.action == 'list':
            return []
        elif self.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return super().get_permissions()
    
    
