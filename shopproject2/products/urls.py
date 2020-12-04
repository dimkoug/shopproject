from django.urls import path

from .views import CategoryDetailView, TagDetailView, ProductDetailView


urlpatterns = [
    path('<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('tag/<str:name>/', TagDetailView.as_view(), name='tag-detail'),

]
