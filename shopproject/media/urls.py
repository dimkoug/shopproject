from django.urls import path, include


app_name = 'media'

urlpatterns = [
    path('api/',include('media.media_api.routers')),
]
