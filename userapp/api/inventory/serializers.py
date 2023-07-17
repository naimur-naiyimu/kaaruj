from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from coreapp.models import Role, User
import userapp
from userapp.models import Notifications


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class AddGroupWithPermissionSerializer(serializers.Serializer):
    data = serializers.JSONField()


class AddRoleSerializer(serializers.Serializer):
    data = serializers.JSONField()


class ViewRoleSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(read_only=True, many=True)
    groups = serializers.StringRelatedField(many=True)  # this will return a list
    # Group_String = serializers.SerializerMethodField()
    class Meta:
        model = Role
        fields = "__all__"
    # def get_Group_String(self, obj):
    #         queryset = Group.objects.filter(id=obj.id)
    #         serializer = GroupSerializer(queryset, many=True)
    #         return serializer.data

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        # fields = ["id", "name"]


class NotificationSerializer(serializers.ModelSerializer):
    # image = serializers.ReadOnlyField(source="created_by.image_url" ,allow_null=True)
    image_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Notifications
        fields = "__all__"
    # def get_image_url(self, obj):
    #     return obj.image.url

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.created_by is None:
            from django.conf  import settings
            return f"{settings.USER_PLACEHOLDER_IMAGE}"
        if obj.created_by.image:
            return request.build_absolute_uri(obj.created_by.image.url)
        else:
            return None
    # def get_image_url(self, instance):
    #     request = self.context["request"]
    #     return [
    #         request.build_absolute_uri(slider_image.image.url)
    #         for slider_image in instance.slider_image.all()
    #     ]


class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.ReadOnlyField(source='role.name')
    image_url = serializers.ReadOnlyField(source='get_image_url')


    class Meta:
        model = User
        fields = "__all__"
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


