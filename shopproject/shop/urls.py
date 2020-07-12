from django.urls import path

from core.patterns import get_patterns

from .views import (
    IndexView, CatalogListView,
    CatalogProductDetailView, OrderListView, BasketView,
    OrderFormView
)

from .functions import (
    remove_from_basket, add_to_basket, clear_basket,
    remove_item_from_basket
)


app_name = 'shop'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('catalog/<slug:slug>/', CatalogProductDetailView.as_view(),
         name='catalog-product-detail'),
    path('basket/items/', BasketView.as_view(), name='basket'),
    path('myorders/items/', OrderListView.as_view(), name='myorders'),
    path('remove_from_basket/<int:id>/', remove_from_basket,
         name='remove_from_basket'),
    path('add_to_basket/<int:id>/', add_to_basket, name='add_to_basket'),
    path('remove_item_from_basket/<int:id>/', remove_item_from_basket,
         name='remove_item_from_basket'),
    path('clear/basket', clear_basket, name='clear-basket'),
    path('order/items/', OrderFormView.as_view(), name='order'),
]

urlpatterns += get_patterns(app_name, 'cms_views', 'shop')
