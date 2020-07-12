from rest_framework import viewsets
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, permissions


from shop.models import (
    Category, Supplier, Brand, BrandSupplier, Specification,
    SpecificationCategory, Attribute, Tag, Product, ProductShipment,
    ProductStatistics, ProductTag, ProductAttribute, ProductCategory,
    ProductMedia, Offer, OfferDetail, Order, OrderStatus, OrderDetail,
    ShoppingCartItem, Hero, HeroItem
)


from .serializers import (
    CategorySerializer, TagSerializer, SpecificationSerializer,
    AttributeSerializer, ProductSerializer, ProductShipmentSerializer,
    SupplierSerializer, BrandSerializer, ProductMediaSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SpecificationViewSet(viewsets.ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductShipmentViewSet(viewsets.ModelViewSet):
    queryset = ProductShipment.objects.all()
    serializer_class = ProductShipmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductMediaViewSet(viewsets.ModelViewSet):
    queryset = ProductMedia.objects.all()
    serializer_class = ProductMediaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
