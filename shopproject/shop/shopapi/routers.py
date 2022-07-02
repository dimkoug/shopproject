from rest_framework import routers

from .viewsets import (
    CategoryViewSet, TagViewSet, FeatureViewSet,
    AttributeViewSet, ProductViewSet, ShipmentViewSet,
    SupplierViewSet, BrandViewSet, MediaViewSet
)


router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'features', FeatureViewSet)
router.register(r'attributes', AttributeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'shipments', ShipmentViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'media', MediaViewSet)

urlpatterns = router.urls
