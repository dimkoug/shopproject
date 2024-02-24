from django.urls import path


app_name = 'baskets'

from .views import BasketView

from .functions import (
    remove_from_basket, add_to_basket, clear_basket,
    remove_item_from_basket, 
)


urlpatterns = [
    path('basket/items/', BasketView.as_view(), name='basket'),
    path('remove_from_basket/<int:id>/', remove_from_basket,
        name='remove_from_basket'),
    path('add_to_basket/<int:id>/', add_to_basket, name='add_to_basket'),
    path('remove_item_from_basket/<int:id>/', remove_item_from_basket,
         name='remove_item_from_basket'),
    path('clear/basket', clear_basket, name='clear-basket'),
]