from django.urls import include, path
from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register(r'', viewsets.OfferViewSet)


urlpatterns = router.urls 
