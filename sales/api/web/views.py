
from . import serializers
from ...models import *
from coreapp.models import User
from coreapp.helper import *
from sales.api.inventory import serializers as inventory_serializers

class InvoiceAPI(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = inventory_serializers.InvoiceSerializer
    permission_classes = [IsAuthenticated,]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['number','created_for']
    http_method_names = ['get']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return  inventory_serializers.InvoiceListSerializer
        else:
            return  inventory_serializers.InvoiceSerializer

    def get_queryset(self):
        return self.queryset.filter(is_custom=False)

    