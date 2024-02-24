import datetime
from django.shortcuts import render
import datetime
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status


from warehouses.models import WareHouse


from .serializers import WareHouseSerializer

class WareHouseViewSet(viewsets.ModelViewSet):
    queryset = WareHouse.objects.all()
    serializer_class = WareHouseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

