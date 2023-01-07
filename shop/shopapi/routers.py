from django.urls import path
from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()


urlpatterns = router.urls +  [
    path('address/list/', viewsets.getAddressList, name='address-list'),
    path('address/create/', viewsets.createAddress, name='address-create'),
    path('address/<str:pk>/', viewsets.getAddress, name='address-detail'),
    path('address/delete/<str:pk>/', viewsets.deleteAddress, name='address-delete'),
    path('address/update/<str:pk>/', viewsets.updateAddress, name='address-update'),


    path('attribute/list/', viewsets.getAttributeList, name='attribute-list'),
    path('attribute/create/', viewsets.createAttribute, name='attribute-create'),
    path('attribute/<str:pk>/', viewsets.getAttribute, name='attribute-detail'),
    path('attribute/delete/<str:pk>/', viewsets.deleteAttribute, name='attribute-delete'),
    path('attribute/update/<str:pk>/', viewsets.updateAttribute, name='attribute-update'),


    path('brand/list/', viewsets.getBrandList, name='brand-list'),
    path('brand/create/', viewsets.createBrand, name='brand-create'),
    path('brand/<str:pk>/', viewsets.getBrand, name='brand-detail'),
    path('brand/delete/<str:pk>/', viewsets.deleteBrand, name='brand-delete'),
    path('brand/update/<str:pk>/', viewsets.updateBrand, name='brand-update'),

    path('category/list/', viewsets.getCategoryList, name='category-list'),
    path('category/create/', viewsets.createCategory, name='category-create'),
    path('category/<str:pk>/', viewsets.getCategory, name='category-detail'),
    path('category/delete/<str:pk>/', viewsets.deleteCategory, name='category-delete'),
    path('category/update/<str:pk>/', viewsets.updateCategory, name='category-update'),    
    
    path('feature/list/', viewsets.getFeatureList, name='feature-list'),
    path('feature/create/', viewsets.createFeature, name='feature-create'),
    path('feature/<str:pk>/', viewsets.getFeature, name='feature-detail'),
    path('feature/delete/<str:pk>/', viewsets.deleteFeature, name='feature-delete'),
    path('feature/update/<str:pk>/', viewsets.updateFeature, name='feature-update'),

    path('hero/list/', viewsets.getHeroList, name='hero-list'),
    path('hero/create/', viewsets.createHero, name='hero-create'),
    path('hero/<str:pk>/', viewsets.getHero, name='hero-detail'),
    path('hero/delete/<str:pk>/', viewsets.deleteHero, name='hero-delete'),
    path('hero/update/<str:pk>/', viewsets.updateHero, name='hero-update'),

    path('logo/list/', viewsets.getLogoList, name='logo-list'),
    path('logo/create/', viewsets.createLogo, name='logo-create'),
    path('logo/<str:pk>/', viewsets.getLogo, name='logo-detail'),
    path('logo/delete/<str:pk>/', viewsets.deleteLogo, name='logo-delete'),
    path('logo/update/<str:pk>/', viewsets.updateLogo, name='logo-update'),


    path('media/list/', viewsets.getMediaList, name='media-list'),
    path('media/create/', viewsets.createMedia, name='media-create'),
    path('media/<str:pk>/', viewsets.getMedia, name='media-detail'),
    path('media/delete/<str:pk>/', viewsets.deleteMedia, name='media-delete'),
    path('media/update/<str:pk>/', viewsets.updateMedia, name='media-update'),


    path('offer/list/', viewsets.getOfferList, name='offer-list'),
    path('offer/create/', viewsets.createOffer, name='offer-create'),
    path('offer/<str:pk>/', viewsets.getOffer, name='offer-detail'),
    path('offer/delete/<str:pk>/', viewsets.deleteOffer, name='offer-delete'),
    path('offer/update/<str:pk>/', viewsets.updateOffer, name='offer-update'),


    path('order/list/', viewsets.getOrderList, name='order-list'),
    path('order/create/', viewsets.createOrder, name='order-create'),
    path('order/<str:pk>/', viewsets.getOrder, name='order-detail'),
    path('order/delete/<str:pk>/', viewsets.deleteOrder, name='order-delete'),
    path('order/update/<str:pk>/', viewsets.updateOrder, name='order-update'),

    path('product/list/', viewsets.getProductList, name='product-list'),
    #path('upload/', views.uploadImage, name='upload'),
    path('product/create/', viewsets.createProduct, name='product-create'),
    #path('top/', views.getTopProducts, name='top-products'),
    #path('<str:pk>/reviews/', views.createProductReview, name='create-review'),
    path('product/<str:pk>/', viewsets.getProduct, name='product-detail'),
    path('product/delete/<str:pk>/', viewsets.deleteProduct, name='product-delete'),
    path('product/update/<str:pk>/', viewsets.updateProduct, name='product-update'),


    path('shipment/list/', viewsets.getShipmentList, name='shipment-list'),
    path('shipment/create/', viewsets.createShipment, name='shipment-create'),
    path('shipment/<str:pk>/', viewsets.getShipment, name='shipment-detail'),
    path('shipment/delete/<str:pk>/', viewsets.deleteShipment, name='shipment-delete'),
    path('shipment/update/<str:pk>/', viewsets.updateShipment, name='shipment-update'),


    path('stock/list/', viewsets.getStockList, name='stock-list'),
    path('stock/create/', viewsets.createStock, name='stock-create'),
    path('stock/<str:pk>/', viewsets.getStock, name='stock-detail'),
    path('stock/delete/<str:pk>/', viewsets.deleteStock, name='stock-delete'),
    path('stock/update/<str:pk>/', viewsets.updateStock, name='stock-update'),


    path('supplier/list/', viewsets.getSupplierList, name='supplier-list'),
    path('supplier/create/', viewsets.createSupplier, name='supplier-create'),
    path('supplier/<str:pk>/', viewsets.getSupplier, name='supplier-detail'),
    path('supplier/delete/<str:pk>/', viewsets.deleteSupplier, name='supplier-delete'),
    path('supplier/update/<str:pk>/', viewsets.updateSupplier, name='supplier-update'),


    path('tag/list/', viewsets.getTagList, name='tag-list'),
    path('tag/create/', viewsets.createTag, name='tag-create'),
    path('tag/<str:pk>/', viewsets.getTag, name='tag-detail'),
    path('tag/delete/<str:pk>/', viewsets.deleteTag, name='tag-delete'),
    path('tag/update/<str:pk>/', viewsets.updateTag, name='tag-update'),

    path('warehouse/list/', viewsets.getWarehouseList, name='warehouse-list'),
    path('warehouse/create/', viewsets.createWarehouse, name='warehouse-create'),
    path('warehouse/<str:pk>/', viewsets.getWarehouse, name='warehouse-detail'),
    path('warehouse/delete/<str:pk>/', viewsets.deleteWarehouse, name='warehouse-delete'),
    path('warehouse/update/<str:pk>/', viewsets.updateWarehouse, name='brand-update'),
]
