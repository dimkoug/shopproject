from django.urls import path


from .functions import get_tags_for_sb

app_name = 'tags'
urlpatterns = [
    path('get_tags_for_sb/', get_tags_for_sb, name='get_tags_for_sb'),
]
