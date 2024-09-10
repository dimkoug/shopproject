from django.urls import path, include

from core.patterns import get_patterns

app_name = 'warehouses'
urlpatterns = [
    path('api/',include('warehouses.warehouses_api.routers')),
]