import datetime
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


from media.models import Media


from .serializers import MediaSerializer


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


