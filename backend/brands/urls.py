from django.urls import path, include


from brands.views import *
from .functions import get_brands_for_sb




app_name = 'brands'
urlpatterns = [

    path('',
         BrandListView.as_view(), name='brand_list'),
    path('add/',
         BrandCreateView.as_view(), name='brand_add'),
    path('view/<int:pk>/',
         BrandDetailView.as_view(), name='brand_view'),
    path('change/<int:pk>/',
         BrandUpdateView.as_view(), name='brand_change'),
    path('delete/<int:pk>/',
         BrandDeleteView.as_view(), name='brand_delete'),
    
    path('sb/', get_brands_for_sb, name='get_brands_for_sb'),
    path('api/',include('brands.brands_api.routers')),
]