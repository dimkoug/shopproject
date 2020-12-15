from rest_framework import routers

from .viewsets import (
    UserViewSet, CategoryViewSet, TagViewSet, SpecificationViewSet,
    AttributeViewSet,ProductViewSet,ProductShipmentViewSet,
    SupplierViewSet, BrandViewSet, ProductMediaViewSet
)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'specifications', SpecificationViewSet)
router.register(r'attributes', AttributeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'productshipments', ProductShipmentViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'productmedia', ProductMediaViewSet)
