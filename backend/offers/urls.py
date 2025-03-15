from django.urls import path, include

from offers.views import *

app_name = 'offers'

urlpatterns = [

    path('',
         OfferListView.as_view(), name='offer_list'),
    path('add/',
         OfferCreateView.as_view(), name='offer_add'),
    path('view/<int:pk>/',
         OfferDetailView.as_view(), name='offer_view'),
    path('change/<int:pk>/',
         OfferUpdateView.as_view(), name='offer_change'),
    path('delete/<int:pk>/',
         OfferDeleteView.as_view(), name='offer_delete'),

     path("add/offerproduct/<int:offer_id>/",add_offer_product,name='add_offerproduct'),

     path("delete/offerproduct/<int:offer_id>/<int:id>/",delete_offer_product,name='delete_offerproduct'),
    path('api/',include('offers.offers_api.routers')),
]
