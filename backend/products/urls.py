from django.urls import path, include

from .views import *

from products.functions import *

app_name = 'products'

urlpatterns = [
    path('categories/',
         CategoryListView.as_view(), name='category_list'),
    path('categories/add/',
         CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/',
         CategoryDetailView.as_view(), name='category_view'),
    path('categories/change/<int:pk>/',
         CategoryUpdateView.as_view(), name='category_change'),
    path('categories/delete/<int:pk>/',
         CategoryDeleteView.as_view(), name='category_delete'),

    path('attributes/',
         AttributeListView.as_view(), name='attribute_list'),
    path('attributes/add/',
         AttributeCreateView.as_view(), name='attribute_add'),
    path('attributes/<int:pk>/',
         AttributeDetailView.as_view(), name='attribute_view'),
    path('attributes/change/<int:pk>/',
         AttributeUpdateView.as_view(), name='attribute_change'),
    path('attributes/delete/<int:pk>/',
         AttributeDeleteView.as_view(), name='attribute_delete'),


    path('features/',
         FeatureListView.as_view(), name='feature_list'),
    path('features/add/',
         FeatureCreateView.as_view(), name='feature_add'),
    path('features/<int:pk>/',
         FeatureDetailView.as_view(), name='feature_view'),
    path('features/change/<int:pk>/',
         FeatureUpdateView.as_view(), name='feature_change'),
    path('features/delete/<int:pk>/',
         FeatureDeleteView.as_view(), name='feature_delete'),

    path('products/',
         ProductListView.as_view(), name='product_list'),
    path('products/add/',
         ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/',
         ProductDetailView.as_view(), name='product_view'),
    path('products/change/<int:pk>/',
         ProductUpdateView.as_view(), name='product_change'),
    path('products/delete/<int:pk>/',
         ProductDeleteView.as_view(), name='product_delete'),



#     path('address/',
#          AddressListView.as_view(), name='address_list'),
#     path('address/add/',
#          AddressCreateView.as_view(), name='address_add'),
#     path('address/<int:pk>/',
#          AddressDetailView.as_view(), name='address_view'),
#     path('address/change/<int:pk>/',
#          AddressUpdateView.as_view(), name='address_change'),
#     path('address/delete/<int:pk>/',
#          AddressDeleteView.as_view(), name='address_delete'),


    
     
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('catalog/<int:pk>/', CatalogProductDetailView.as_view(),
         name='catalog-product-detail'),
    path('address/create/', SiteAddressCreateView.as_view(),
         name='site-address-add'),
    path('address/<int:pk>/update/', SiteAddressUpdateView.as_view(),
         name='site-address-update'),
    path('address/<int:pk>/delete/', SiteAddressDeleteView.as_view(),
         name='site-address-delete'),
    path('myorders/items/', OrderListView.as_view(), name='myorders'),
    path('order/items/', OrderFormView.as_view(), name='order'),
    path('search/', search_items, name="search"),

     path('sb/',get_products_for_sb, name='sb-products'),
     path('features/sb/',get_features_for_sb, name='sb-features'),
     path('categories/sb/',get_categories_for_sb, name='sb-categories'),
     path("delete/media/<int:product_id>/<int:media_id>/",delete_media,name='form-delete-media'),
     path("delete/logo/<int:product_id>/<int:logo_id>/",delete_logo,name='form-delete-logo'),
     path("delete/attribute/<int:product_id>/<int:attribute_id>/",delete_attribute,name='form-delete-attribute'),
     path("create/attribute/<int:product_id>/",create_product_attribute,name='form-create-attribute'),
     path("generate_pdf/<int:product_id>/",generate_pdf,name='generate-pdf'),

     path("create/feature/attribute/<int:feature_id>/",create_feature_attribute, name="add-feature-attribute"),


    path('api/',include('products.productsapi.routers')),
]
