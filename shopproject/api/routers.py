from django.urls import path
from rest_framework import routers

from heroes.heroes_api.viewsets import *
from logos.logos_api.viewsets import *
from offers.offers_api.viewsets import *
from orders.orders_api.viewsets import *
from shipments.shipments_api.viewsets import *
from shop.shopapi.viewsets import *
from stocks.stocks_api.viewsets import *
from suppliers.suppliers_api.viewsets import *
from tags.tags_api.viewsets import *
from warehouses.warehouses_api.viewsets import *
from users.users_api.viewsets import *

router = routers.DefaultRouter()

router.register(r'heroes',HeroViewSet)
router.register(r'logos',LogoViewSet)
router.register(r'offers',OfferViewSet)
router.register(r'orders',OrderViewSet)
router.register(r'shipments',ShipmentViewSet)
router.register(r'attributes', AttributeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'features', FeatureViewSet)
router.register(r'media', MediaViewSet)
router.register(r'products', ProductViewSet)

router.register(r'stocks', StockViewSet)

router.register(r'suppliers', SupplierViewSet)
router.register(r'tags', TagViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
urlpatterns = router.urls + [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('current_user/', current_user),
    path('register/', RegisterApi.as_view()),
    # path('users/', UserList.as_view())
]
