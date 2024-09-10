from django.urls import path, include


app_name = 'shipments'

urlpatterns = [
    path('api/',include('shipments.shipments_api.routers')),
]
