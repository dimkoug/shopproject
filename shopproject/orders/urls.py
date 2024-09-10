from django.urls import path, include


app_name = 'orders'

urlpatterns = [
    path('api/',include('orders.orders_api.routers')),
]
