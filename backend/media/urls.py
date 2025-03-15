from django.urls import path, include

from media.views import *

app_name = 'media'

urlpatterns = [
    path('',
         MediaListView.as_view(), name='media_list'),
    path('add/',
         MediaCreateView.as_view(), name='media_add'),
    path('view/<int:pk>/',
         MediaDetailView.as_view(), name='media_view'),
    path('change/<int:pk>/',
         MediaUpdateView.as_view(), name='media_change'),
    path('delete/<int:pk>/',
         MediaDeleteView.as_view(), name='media_delete'),
    path('api/',include('media.media_api.routers')),
]
