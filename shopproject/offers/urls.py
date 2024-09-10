from django.urls import path, include


app_name = 'offers'

urlpatterns = [
    path('api/',include('offers.offers_api.routers')),
]
