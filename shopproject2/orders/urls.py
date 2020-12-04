from django.urls import Path

from .views import OrderListView, order,remove_from_basket,add_to_basket,basket

urlpatterns =[
    path('basket/items/', basket, name='basket'),
    path('myorders/items/', OrderListView.as_view(), name='myorders'),
    path('remove_from_basket/<int:id>/', remove_from_basket, name='remove_from_basket'),
    path('add_to_basket/<int:id>/', add_to_basket, name='add_to_basket'),
    path('order/items/', order, name='order'),
]
