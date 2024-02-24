from django.urls import path

from .views import (
    IndexView, CatalogListView,
    CatalogProductDetailView, OrderListView, BasketView,
    OrderFormView, AddressCreateView as SiteAddressCreateView,
    AddressUpdateView as SiteAddressUpdateView,
    AddressDeleteView as SiteAddressDeleteView,
    search_items,
)

from .functions import (
    remove_from_basket, add_to_basket, clear_basket,
    remove_item_from_basket, 
    get_products_for_sb,
    get_categories_for_sb,
    get_attributes_for_sb,
    get_attributes,
    set_attribute,
    delete_attribute,
)


app_name = 'shop'

urlpatterns = [
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('catalog/<int:pk>/', CatalogProductDetailView.as_view(),
         name='catalog-product-detail'),
    path('basket/items/', BasketView.as_view(), name='basket'),
    path('address/create/', SiteAddressCreateView.as_view(),
         name='site-address-add'),
    path('address/<int:pk>/update/', SiteAddressUpdateView.as_view(),
         name='site-address-update'),
    path('address/<int:pk>/delete/', SiteAddressDeleteView.as_view(),
         name='site-address-delete'),
    path('myorders/items/', OrderListView.as_view(), name='myorders'),
    path('remove_from_basket/<int:id>/', remove_from_basket,
         name='remove_from_basket'),
    path('add_to_basket/<int:id>/', add_to_basket, name='add_to_basket'),
    path('remove_item_from_basket/<int:id>/', remove_item_from_basket,
         name='remove_item_from_basket'),
    path('clear/basket', clear_basket, name='clear-basket'),
    path('order/items/', OrderFormView.as_view(), name='order'),
    path('search/', search_items, name="search"),

    path('get_products_for_sb/',get_products_for_sb, name='get_products_for_sb'),
    path('get_attributes_for_sb/', get_attributes_for_sb, name='get_attributes_for_sb'),
    path('get_categories_for_sb/', get_categories_for_sb, name='get_categories_for_sb'),
    path('attributes/', get_attributes, name='get_attributes'),
    path('set_attribute/', set_attribute, name='set_attributes'),
    path('delete_attribute/', delete_attribute, name='delete_attributes'),
]
