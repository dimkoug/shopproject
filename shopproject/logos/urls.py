from django.urls import path, include


app_name = 'logos'

urlpatterns = [
    path('api/',include('logos.logos_api.routers')),
]
