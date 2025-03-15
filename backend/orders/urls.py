from django.urls import path, include


from orders.views import *


app_name = 'orders'

urlpatterns = [
    path('',
         OrderListView.as_view(), name='order_list'),
    path('add/',
         OrderCreateView.as_view(), name='order_add'),
    path('view/<int:pk>/',
         OrderDetailView.as_view(), name='order_view'),
    path('change/<int:pk>/',
         OrderUpdateView.as_view(), name='order_change'),
    path('delete/<int:pk>/',
         OrderDeleteView.as_view(), name='order_delete'),
    path('model/order/', model_order, name='model_order'),
    path('api/',include('orders.orders_api.routers')),
]
