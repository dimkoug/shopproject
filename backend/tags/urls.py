from django.urls import path, include


from tags.views import *

from .functions import get_tags_for_sb

app_name = 'tags'
urlpatterns = [
    path('',
         TagListView.as_view(), name='tag_list'),
    path('add/',
         TagCreateView.as_view(), name='tag_add'),
    path('view/<int:pk>/',
         TagDetailView.as_view(), name='tag_view'),
    path('change/<int:pk>/',
         TagUpdateView.as_view(), name='tag_change'),
    path('delete/<int:pk>/',
         TagDeleteView.as_view(), name='tag_delete'),
    
    path('get_tags_for_sb/', get_tags_for_sb, name='get_tags_for_sb'),
    path('api/',include('tags.tags_api.routers')),
]
