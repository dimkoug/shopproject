from .address import AddressListView, AddressDetailView, AddressCreateView, AddressUpdateView, AddressDeleteView
from .attribute import AttributeListView, AttributeDetailView, AttributeCreateView, AttributeUpdateView, AttributeDeleteView, create_attribute,delete_attribute
from .brand import BrandListView, BrandDetailView, BrandCreateView, BrandUpdateView, BrandDeleteView
from .category import CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
from .core import ManageView
from .feature import FeatureListView, FeatureDetailView, FeatureCreateView, FeatureUpdateView, FeatureDeleteView, create_featurecategory,delete_featurecategory
from .hero import HeroListView, HeroDetailView, HeroCreateView, HeroUpdateView, HeroDeleteView
from .product import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView
from .tag import TagListView, TagDetailView, TagCreateView, TagUpdateView, TagDeleteView
from .supplier import SupplierListView, SupplierDetailView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView
from .warehouse import WarehouseListView, WarehouseDetailView, WarehouseCreateView, WarehouseUpdateView, WarehouseDeleteView
from .media import MediaListView, MediaDetailView, MediaCreateView, MediaUpdateView, MediaDeleteView
from .logo import LogoListView, LogoDetailView, LogoCreateView, LogoUpdateView, LogoDeleteView
from .stock import StockListView, StockDetailView, StockCreateView, StockUpdateView, StockDeleteView
from .shipment import ShipmentListView, ShipmentDetailView, ShipmentCreateView, ShipmentUpdateView, ShipmentDeleteView
from .offer import OfferListView, OfferDetailView, OfferCreateView, OfferUpdateView, OfferDeleteView
from .order import OrderListView, OrderDetailView, OrderCreateView, OrderUpdateView, OrderDeleteView, model_order
