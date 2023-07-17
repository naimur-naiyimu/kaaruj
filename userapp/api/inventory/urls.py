
from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers
router = routers.DefaultRouter()
# router.register(r'getuser', views.GetUserView, basename='user-get')
router.register(r'role', views.DeleteRoleView, basename='role-delete')
router.register(r'notifications', views.NotificationsViewSet, basename='notifications')
# router.register(r'user2', views.UserUpdateGetViewSet, basename='user2')
# router.register(r'groups', views.GroupViewSet, basename='group')

urlpatterns = [
    path("group/", views.GroupView.as_view(), name="groups"),
    path("group/<int:pk>/", views.GroupUpdateView.as_view(), name="groups-update"),
    path("model/", views.ModelView.as_view(), name="models"),
    # path("user/", views.UserView.as_view(), name="users"),
    path("user/<str:pk>/", views.UserRetrieveDeleteUpdate.as_view(), name="users-details"),
    path("user/", views.UserView.as_view(), name="users"),
    path("role/", views.AddRoleView.as_view(), name="role")
]
urlpatterns += router.urls
