
from . import serializers
from ...models import *
from coreapp.models import User
from coreapp.helper import *
from .. import filters as custom_filters

class ProductAPI(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class  = custom_filters.ProductFilter
    search_fields = ['name', 'description']
    lookup_field = 'slug'
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class CategoryAPI(viewsets.ModelViewSet):
    '''
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
    '''
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = ['level','main_category','sub_main_category','category_type']
    lookup_field = 'slug'
    http_method_names = ['get']



class AttributeAPI(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Attributes.objects.all()
    serializer_class = serializers.AttributeSerializer
    http_method_names = ['get']
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    

class AttributeValueAPI(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = AttributeValue.objects.all()
    serializer_class = serializers.AttributeValueSerializer
    http_method_names = ['get']

class TagsAPI(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Tags.objects.all()
    serializer_class = serializers.TagsSerializer
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = custom_filters.TagsFilter