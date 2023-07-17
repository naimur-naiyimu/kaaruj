
from . import serializers
from ...models import *
from coreapp.models import User
from coreapp.helper import *



class ProductAPI(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsAuthenticated]


class CategoryAPI(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAuthenticated]