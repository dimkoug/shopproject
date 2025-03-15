from django.urls import path, include



from addresses.views import *

app_name = 'addresses'

urlpatterns = [
    path('',
         AddressListView.as_view(), name='address_list'),
    path('add/',
         AddressCreateView.as_view(), name='address_add'),
    path('view/<int:pk>/',
         AddressDetailView.as_view(), name='address_view'),
    path('change/<int:pk>/',
         AddressUpdateView.as_view(), name='address_change'),
    path('delete/<int:pk>/',
         AddressDeleteView.as_view(), name='address_delete'),
    path('api/',include('addresses.addresses_api.routers')),
]
