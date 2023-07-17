from rest_framework.permissions import DjangoModelPermissions,SAFE_METHODS
from rest_framework import permissions


class CustomDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

class OwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
# class OwnerOnly(permissions.BasePermission):
#      def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request,
#         # so we'll always allow GET, HEAD or OPTIONS requests.
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # Instance must have an attribute named `owner`.
#         return obj.owner == request.user
    # def has_permission(self, request, view):
    #     # work when your access /item/
    #     print("working")
    #     if request.user:
    #         return True
    #     else:
    #         return False

    # def has_object_permission(self, request, view, obj):
    #     print("working2")
        
    #     return obj.owner == request.user
