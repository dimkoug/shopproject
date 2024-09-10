from django.urls import path, include

from .functions import get_brands_for_sb

app_name = 'brands'
urlpatterns = [
    path('sb/', get_brands_for_sb, name='get_brands_for_sb'),
    path('api/',include('brands.brands_api.routers')),
]