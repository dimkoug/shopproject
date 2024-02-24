from django.urls import path
from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()
router.register(r'attributes', viewsets.AttributeViewSet)
router.register(r'categories', viewsets.CategoryViewSet)
router.register(r'features', viewsets.FeatureViewSet)
router.register(r'media', viewsets.MediaViewSet)
router.register(r'products', viewsets.ProductViewSet)


urlpatterns = router.urls
