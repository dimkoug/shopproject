from django.urls import path, include


app_name = 'addresses'

urlpatterns = [
    path('api/',include('addresses.addresses_api.routers')),
]
