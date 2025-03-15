from django.urls import path, include


from logos.views import *


app_name = 'logos'

urlpatterns = [
    path('',
         LogoListView.as_view(), name='logo_list'),
    path('add/',
         LogoCreateView.as_view(), name='logo_add'),
    path('view/<int:pk>/',
         LogoDetailView.as_view(), name='logo_view'),
    path('change/<int:pk>/',
         LogoUpdateView.as_view(), name='logo_change'),
    path('delete/<int:pk>/',
         LogoDeleteView.as_view(), name='logo_delete'),
    path('api/',include('logos.logos_api.routers')),
]
