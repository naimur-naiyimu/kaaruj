from django.shortcuts import render
import traceback
from urllib import response
from django.shortcuts import render
from rest_framework import viewsets
from userapp.models import Notifications
from . import serializers
from coreapp.helper import *
from django.contrib.auth.models import Group, Permission
from userapp.models import GroupTime
from coreapp.models import Role, User
from rest_framework.authtoken.models import Token

class GroupView(views.APIView):
    permission_classes = (CustomDjangoModelPermissions, IsAuthenticated)

    def get_queryset(self):
        return Group.objects.all()

    @extend_schema(request=serializers.GroupSerializer, responses={201: serializers.GroupSerializer})
    def get(self, request, format=None):
        try:
            pk = request.GET.get("id")
            if (pk is None):
                queryset = Group.objects.all()
            else:
                queryset = Group.objects.filter(id=pk)
            data = []
            for group in queryset:
                group_time = GroupTime.objects.filter(group_id=group.id).first()
                if group_time is not None:

                    permissions_data = []
                    current_data = {
                        'id': group.id,
                        'name': group.name,
                        'permissions': [],
                        'created_at': group_time.created_at,
                        'updated_at': group_time.updated_at,
                    }
                    for permissions in group.permissions.all():
                        permissions_data.append({
                            'id': permissions.id,
                            "name": permissions.name,
                            "content_type": permissions.content_type.name,
                            "codename": permissions.codename,
                        })
                        current_data["permissions"] = permissions_data
                    data.append(current_data)

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            data = {
                "msg": "Data Doesn't Exists",
                'error': str(e)
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=serializers.AddGroupWithPermissionSerializer, responses={201: serializers.AddGroupWithPermissionSerializer})
    def post(self, request, format=None):
        try:
            GROUPS = request.data
            print(GROUPS)

            for group_name in GROUPS:
                print("group_name", group_name)

                new_group = Group.objects.filter(name=group_name).first()

                if new_group is None:
                    new_group = Group.objects.create(name=group_name)
                    group_time = GroupTime.objects.create(group_id=new_group.id)
                else:
                    data = {
                        "error": "Group with this same name already exists."
                    }
                    return Response(data, status=status.HTTP_404_NOT_FOUND)

                # Loop models in group
                for app_model in GROUPS[group_name]:
                    print("app_model", app_model)

                    # Loop permissions in group/model
                    for permission_name in GROUPS[group_name][app_model]:

                        # Generate permission name as Django would generate it
                        name = f"Can {permission_name} {app_model.lower()}"
                        print(name)

                        try:
                            model_add_perm = Permission.objects.get(name=name)
                        except Permission.DoesNotExist:
                            print("Permission not found with name '{}'.".format(name))
                            continue

                        new_group.permissions.add(model_add_perm)
            data = {
                "id": new_group.id,
                "group": new_group.name,



            }
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as e:
            traceback.print_exc()
            data = {
                "msg": "Something went wrong.",
                "error": str(e)
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class GroupUpdateView(views.APIView):
    @extend_schema(request=serializers.AddGroupWithPermissionSerializer, responses={201: serializers.AddGroupWithPermissionSerializer})
    def patch(self, request, pk, format=None):
        try:
            GROUPS = request.data
            print("GROUPS", GROUPS)

            for group_name in GROUPS:
                foundGroup = Group.objects.filter(id=pk).first()
                foundGroup.name = group_name
                foundGroup.permissions.clear()
                # foundGroup.permissions.clear()
                # print("Found group users => ",foundGroup.user_set.all())
                grouped_users = foundGroup.user_set.all()
                for userss in grouped_users:
                    userToken = Token.objects.filter(user_id=userss.id).first()
                    if userToken is not None:
                        userToken.delete()

                if foundGroup is not None:
                    print("group_name", group_name)

                    # Loop models in group
                    for app_model in GROUPS[group_name]:
                        print("app_model", app_model)

                        # Loop permissions in group/model
                        for permission_name in GROUPS[group_name][app_model]:

                            # Generate permission name as Django would generate it
                            name = f"Can {permission_name} {app_model.lower()}"
                            print(name)

                            try:
                                model_add_perm = Permission.objects.get(name=name)
                            except Permission.DoesNotExist:
                                print("Permission not found with name '{}'.".format(name))
                                continue

                            foundGroup.permissions.add(model_add_perm)
                foundGroup.save()

                return Response({"data": "updated"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            traceback.print_exc()
            data = {
                "msg": "Something went wrong.",
                "error": str(e)
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=serializers.AddGroupWithPermissionSerializer, responses={201: serializers.AddGroupWithPermissionSerializer})
    def delete(self, request, pk, format=None):
        try:
            foundGroup = Group.objects.filter(id=pk).first()

            if foundGroup is not None:
                foundGroup.permissions.clear()
                grouped_users = foundGroup.user_set.all()
                for userss in grouped_users:
                    userToken = Token.objects.filter(user_id=userss.id).first()
                    if userToken is not None:
                        userToken.delete()
                foundGroup.delete()
                return Response({"data": "deleted"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"data": "deleted", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # @extend_schema(request=serializers.GroupSerializer, responses={201: serializers.GroupSerializer})
    # def post(self, request, format=None):
    #     serializer = serializers.GroupSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'data': serializer.data, "msg": "Created"}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Can view products
# can view Products -->wrong


class ModelView(views.APIView):
    permission_classes = (CustomDjangoModelPermissions, IsAuthenticated)

    def get_queryset(self):
        return Permission.objects.all()

    def get(self, request, format=None):
        try:
            # queryset = Permission.objects.all()
            # print("+============")
            # print(queryset)
            # print("+============")
            # data = []
            # from django.contrib.contenttypes.models import ContentType
            # exclude_models = ['auth', 'logentry', 'sessions', 'auth_token', "sessions", "contenttypes", "admin"]
            # for contentT in ContentType.objects.all():
            #     mo_del = contentT.model_class()
            #     if mo_del.__name__ not in exclude_models:
            #         data.append(mo_del.__name__)
            from django.apps import apps

            app_models = [model.__name__ for model in apps.get_models()]
            return Response(app_models, status=status.HTTP_200_OK)

        except:
            traceback.print_exc()
            data = {
                "msg": "Data Doesn't Exists"
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)


class AddRoleView(views.APIView):

    permission_classes = (CustomDjangoModelPermissions, IsAuthenticated)

    def get_queryset(self):
        return Role.objects.all()

    @extend_schema(request=serializers.ViewRoleSerializer, responses={201: serializers.ViewRoleSerializer})
    def get(self, request):
        roles = Role.objects.all()
        serializer = serializers.ViewRoleSerializer(roles, many=True)
        serializer = serializers.ViewRoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=serializers.AddRoleSerializer, responses={201: serializers.AddRoleSerializer})
    def post(self, request,):
        try:
            roles_data = request.data
            if not Role.objects.filter(name=roles_data['name']).exists():
                role = Role.objects.create(name=roles_data['name'])

                for group in roles_data['roles']:
                    group_obj = Group.objects.get(id=group)
                    role.groups.add(group_obj)
                role.save()
                data = {
                    "id": role.id,
                    "role": role.name,
                    "created_at": role.created_at,
                    "updated_at": role.updated_at,

                }
                return Response(data, status=status.HTTP_201_CREATED)
            return Response({"msg": "Already exists a role with this same name."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            traceback.print_exc()
            data = {
                "msg": "Something went wrong."
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

import datetime
class UserView(views.APIView, LimitOffsetPagination):
    permission_classes = (CustomDjangoModelPermissions, IsAuthenticated)

    def get_queryset(self):
        return User.objects.all()

    @extend_schema(request=serializers.UserSerializer, responses={201: serializers.UserSerializer})
    def get(self, request, format=None):
        try:
            start = request.GET.get("start",None)
            end = request.GET.get("end",None)
            queryset = User.objects.all()

            # results = self.paginate_queryset(queryset, request, view=self)
            serializer = serializers.UserSerializer(queryset, many=True)
            if start is None and end is None:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                if start is not None:
                    start_month, start_day,  start_year = start.split("/")
                else:
                    return Response({"data": [], "error": "Start date is empty or Please use correct format,month/date/year"}, status=status.HTTP_404_NOT_FOUND)
                if end is not None:

                    end_month, end_day,  end_year = end.split("/")
                else:
                    return Response({"data": [], "error": "End date is empty or Please use correct format,month/date/year"}, status=status.HTTP_404_NOT_FOUND)
                start_date = datetime.datetime(year=int(start_year), month=int(start_month), day=int(start_day),
                                               hour=0, minute=0, second=0)  # represents 00:00:00
                end_date = datetime.datetime(year=int(end_year), month=int(end_month), day=int(end_day),
                                             hour=23, minute=59, second=59)
                queryset = User.objects.filter(created_at__range=[start_date, end_date])
                print("queryset",queryset)
                serializer = serializers.UserSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            data = {
                "msg": "Data Doesn't Exists",
                'error': str(e)
            }

            return Response(data, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=serializers.UserSerializer, responses={201: serializers.UserSerializer})
    def post(self, request, format=None):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user_id = serializer.data['id']
            user_pass = serializer.data["password"]
            user_role = serializer.data['role']
            # groups = User.objects.
            user = User.objects.get(id=user_id)
            user.set_password(user_pass)
            user.save()

            role = Role.objects.get(id=user_role)
            print(role)
            print(role.groups)
            count = 0

            for group in role.groups.all():
                my_group = Group.objects.get(name=group.name)
                my_group.user_set.add(user)
                # groupForInsert = Group.objects.get(name=group.name)
                # user.groups.add(groupForInsert)

                # for perm in groupForInsert.permissions.all():

                #     user.user_permissions.add(perm)
            user.save()

            return Response({'data': serializer.data, "msg": "Created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveDeleteUpdate(views.APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(slug=pk)
        except User.DoesNotExist:
            raise Http404

    @extend_schema(request=serializers.UserSerializer, responses={201: serializers.UserSerializer})
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializers.UserSerializer(snippet)
        return Response(serializer.data)

    @extend_schema(request=serializers.UserSerializer, responses={201: serializers.UserSerializer})
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = serializers.UserSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=serializers.UserSerializer, responses={201: serializers.UserSerializer})
    def patch(self, request, pk, format=None):
        print("request", request.data)
        snippet = self.get_object(pk)
        new_password = request.data.get("password")
        serializer = serializers.UserSerializer(snippet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            try:
                user_id = serializer.data['id']
                user_pass = serializer.data["password"]
                user_request_pass = request.data.get("password")
                user_role = serializer.data['role']
                # groups = User.objects.
                user = User.objects.get(id=user_id)
                if new_password != "" and new_password is not None:
                    user.set_password(new_password)

                print("user password == >", user_pass)
                print("user request password == >", new_password)

                user.user_permissions.clear()  # cleared previous relationships
                user.groups.clear()

                role = Role.objects.get(id=user_role)
                for group in role.groups.all():
                    my_group = Group.objects.get(name=group.name)
                    my_group.user_set.add(user)
                    my_group.save()
                userToken = Token.objects.filter(user_id=user_id).first()
                if userToken is not None:
                    userToken.delete()

                # role = Role.objects.get(id=user_role)
                # print("role name ", role)
                # count = 0
                # for group in role.groups.all():
                #     groupForInsert = Group.objects.get(name=group.name)
                #     print("group", groupForInsert)
                #     user.groups.add(groupForInsert)

                #     for perm in groupForInsert.permissions.all():

                #         user.user_permissions.add(perm)
                user.save()

            except:
                traceback.print_exc()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteUserView(viewsets.ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions, IsAuthenticated)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    http_method_names = ['delete']


class DeleteRoleView(viewsets.ModelViewSet):
    permission_classes = (CustomDjangoModelPermissions, IsAuthenticated)
    queryset = Role.objects.all()
    serializer_class = serializers.ViewRoleSerializer
    http_method_names = ['delete']

    def destroy(self, request, *args, **kwargs):
        try:
            role = self.get_object()
            connectedUsers = User.objects.filter(role_id=role.id)
            # default = Category.objects.filter(name="Category Deleted").first()
            # if default is None:
            #         default = Category.objects.create(name="Category Deleted")
            for user in connectedUsers:
                userToken = Token.objects.filter(user_id=user.id).first()
                if userToken is not None:
                    userToken.delete()
            role.delete()
            return Response("Deleted", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_200_OK)


# GROUPS = {
#     "Administration": {
#         # general permissions
#         "log entry": ["add", "delete", "change", "view"],
#         "group": ["add", "delete", "change", "view"],
#         "permission": ["add", "delete", "change", "view"],
#         "user": ["add", "delete", "change", "view"],
#         "content type": ["add", "delete", "change", "view"],
#         "session": ["add", "delete", "change", "view"],

#         # django app model specific permissions
#         "project": ["add", "delete", "change", "view"],
#         "order": ["add", "delete", "change", "view"],
#         "staff time sheet": ["add", "delete", "change", "view"],
#         "staff": ["add", "delete", "change", "view"],
#         "client": ["add", "delete", "change", "view"],
#     }, }

# class PermissionAddToGroupView(views.APIView):
#     permission_classes = [IsAuthenticated]


class NotificationsViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for Notifications.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Notifications.objects.all()
    serializer_class = serializers.NotificationSerializer
    http_method_names = ['get',  'delete']

    @action(detail=False, methods=['delete'])
    def clear_all(self, request):
        Notifications.objects.all().delete()
        return Response({"data": "All Notifications Deleted "}, status=status.HTTP_200_OK)
