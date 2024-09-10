from django.urls import path, include


from .functions import get_tags_for_sb

app_name = 'tags'
urlpatterns = [
    path('get_tags_for_sb/', get_tags_for_sb, name='get_tags_for_sb'),
    path('api/',include('tags.tags_api.routers')),
]
