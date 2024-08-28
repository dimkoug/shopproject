from django.urls import path
from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()
router.register(r'warehouses', viewsets.WarehouseViewSet)
urlpatterns = router.urls 