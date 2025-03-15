from django.urls import path
from rest_framework import routers

from .viewsets import *

router = routers.DefaultRouter()

router.register(r'attributes', AttributeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'features', FeatureViewSet)
router.register(r'products', ProductViewSet)


urlpatterns = router.urls