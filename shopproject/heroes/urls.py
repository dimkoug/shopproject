from django.urls import path, include


app_name = 'heroes'

urlpatterns = [
    path('api/',include('heroes.heroes_api.routers')),
]
