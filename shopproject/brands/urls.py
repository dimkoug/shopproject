from django.urls import path

from .functions import get_brands_for_sb

app_name = 'brands'
urlpatterns = [
    path('get_brands_for_sb/', get_brands_for_sb, name='get_brands_for_sb'),
]