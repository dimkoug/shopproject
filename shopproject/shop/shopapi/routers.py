from django.urls import path
from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()
router.register(r'attributes', viewsets.AttributeViewSet)
router.register(r'address', viewsets.AddressViewSet)
router.register(r'brands', viewsets.BrandViewSet)
router.register(r'categories', viewsets.CategoryViewSet)
router.register(r'features', viewsets.FeatureViewSet)
router.register(r'heroes', viewsets.HeroViewSet)
router.register(r'logos', viewsets.LogoViewSet)
router.register(r'media', viewsets.MediaViewSet)
router.register(r'offers', viewsets.OfferViewSet)
router.register(r'orders', viewsets.OrderViewSet)
router.register(r'products', viewsets.ProductViewSet)
router.register(r'shipments', viewsets.ShipmentViewSet)
router.register(r'stocks', viewsets.StockViewSet)
router.register(r'suppliers', viewsets.SupplierViewSet)
router.register(r'tags', viewsets.TagViewSet)
router.register(r'warehouses', viewsets.WareHouseViewSet)


urlpatterns = router.urls 