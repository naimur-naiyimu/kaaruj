from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, views, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django_filters import rest_framework as dj_filters
from . import serializers
from .. import filters
from ...models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class GlobalSettingsAPI(views.APIView):
    permission_classes = [IsAdminUser, ]

    @extend_schema(
        responses={200: serializers.GlobalSettingsSerializer}
    )
    def get(self, request):
        global_settings = GlobalSettings.objects.first()
        serializer = serializers.GlobalSettingsSerializer(global_settings)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={200: serializers.GlobalSettingsSerializer},request=serializers.GlobalSettingsSerializer )
    def post(self, request):
        global_settings = GlobalSettings.objects.first()
        serializer = serializers.GlobalSettingsSerializer(data=request.data, instance=global_settings)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PageAdminAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Page.objects.all()
    serializer_class = serializers.PageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['page_type','is_active']

class SocialMediaAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = SocialMedia.objects.all()
    serializer_class = serializers.SocialMediaSerializer


class TestimonialAdminAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Testimonial.objects.all()
    serializer_class = serializers.TestimonialSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'designation',]

class SliderAdminAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Slider.objects.all()
    serializer_class = serializers.SliderSerializer


class TeamMemberAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = TeamMember.objects.all()
    serializer_class = serializers.TeamMemberSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'designation',]

class ContactUsAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Contact.objects.all()
    serializer_class = serializers.ContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'email', 'mobile', 'message']
    filterset_fields = ['contact_type']



class DisplayCenterAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    queryset = Display_Center.objects.all()
    serializer_class = serializers.DisplayCenterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'location', 'mobile']
