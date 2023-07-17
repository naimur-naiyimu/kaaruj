from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, views
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django_filters import rest_framework as dj_filters
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.decorators import action
from coreapp.pagination import paginate
from rest_framework.pagination import LimitOffsetPagination
from django.db.models.functions import Now
from django.db.models import Q, Sum, Count, Avg, Max, Min
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import mixins, status
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models.signals import pre_save, post_save
from rest_framework import filters
from itertools import product
from django.db import models
from io import BytesIO
from django.core.files import File
from django.utils.timezone import now
from urllib import response
import traceback
from rest_framework import permissions
from functools import partial
from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from drf_spectacular.utils import extend_schema
import csv
from django.http import FileResponse, Http404
from utility.utils.permissions_utils import *
from django.utils.crypto import get_random_string
from PIL import Image

from coreapp.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings


def print_log(log):
    import logging
    logger = logging.getLogger('django')
    logger.error(log)