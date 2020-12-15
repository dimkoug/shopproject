from rest_framework import  viewsets
from users.models import User

from products.models import (Category, Tag, Specification, Attribute,
                             Product,ProductTag, ProductShipment,
                             Supplier, BrandSupplier, ProductAttribute,
                             ProductCategory, Brand, ProductMedia)


from .serializers import (
    UserSerializer, CategorySerializer, TagSerializer, SpecificationSerializer,
    AttributeSerializer,ProductSerializer,ProductShipmentSerializer,
    SupplierSerializer, BrandSerializer, ProductMediaSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class SpecificationViewSet(viewsets.ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer

class AttributeViewSet(viewsets.ModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductShipmentViewSet(viewsets.ModelViewSet):
    queryset = ProductShipment.objects.all()
    serializer_class = ProductShipmentSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductMediaViewSet(viewsets.ModelViewSet):
    queryset = ProductMedia.objects.all()
    serializer_class = ProductMediaSerializer
