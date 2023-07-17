from coreapp.api.serializers import DocumentSerializer
from inventory.models import *
from rest_framework import serializers
from ...models import *

class SliderSerializer(serializers.ModelSerializer):
    thumb_url = serializers.CharField(source='get_image_url', read_only=True)
    class Meta:
        model = Slider
        fields = '__all__'

class PageSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(source='get_video_url', read_only=True)
    thumbnail_url = serializers.CharField(source='get_thumbnail_url', read_only=True)
    slider_details = SliderSerializer(read_only=True,many=True,source='get_sliders')
    class Meta:
        model = Page
        fields = '__all__'
    
    def validate(self, data):
        page_type = data.get('page_type')
        is_active = data.get('is_active')
        instance = self.instance

        if page_type and is_active:
            existing_active_data = Page.objects.filter(page_type=page_type, is_active=True)
            if instance:
                existing_active_data = existing_active_data.exclude(id=instance.id)

            if existing_active_data.exists():
                raise serializers.ValidationError("An active data with the same page_type already exists.")
        return data


class SocialMediaSerializer(serializers.ModelSerializer):
    thumb_url = serializers.CharField(source='get_thumb_url', read_only=True)
    class Meta:
        model = SocialMedia
        fields = '__all__'


class TeamMemberSerializer(serializers.ModelSerializer):
    thumb_url = serializers.CharField(source='get_thumb_url', read_only=True)

    class Meta:
        model = TeamMember
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    thumb_url = serializers.CharField(source='get_thumb_url', read_only=True)

    class Meta:
        model = Testimonial
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    document_details = DocumentSerializer(read_only=True,source='document')
    class Meta:
        model = Contact
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class GlobalSettingsSerializer(serializers.ModelSerializer):
    video_url = serializers.CharField(source='get_video_url', read_only=True)
    about_us_image_url = serializers.CharField(source='get_about_us_image_url', read_only=True)
    logo_url = serializers.CharField(source='get_logo_url', read_only=True)
    brand_url = DocumentSerializer(read_only=True,source='brand_images',many=True)
    payment_method_images_url = serializers.ReadOnlyField(source='get_payment_method_images_url')
    qr_code_url = serializers.ReadOnlyField(source='get_qr_code_url')
    class Meta:
        model = GlobalSettings
        fields = '__all__'
class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'




class DisplayCenterSerializer(serializers.ModelSerializer):
    thumb_url = serializers.CharField(source='get_thumb_url', read_only=True)
    class Meta:
        model = Display_Center
        fields = '__all__'
