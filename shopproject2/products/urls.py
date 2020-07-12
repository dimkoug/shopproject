from django.urls import path

from .views import CategoryDetailView, OrderListView, TagDetailView, ProductDetailView, add_to_basket,  remove_from_basket, basket, order


urlpatterns = [
    path('basket/items/', basket, name='basket'),
    path('myorders/items/', OrderListView.as_view(), name='myorders'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('tag/<str:name>/', TagDetailView.as_view(), name='tag-detail'),
    path('remove_from_basket/<int:id>/', remove_from_basket, name='remove_from_basket'),
    path('add_to_basket/<int:id>/', add_to_basket, name='add_to_basket'),
    path('order/items/', order, name='order'),
]
