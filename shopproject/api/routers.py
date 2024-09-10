from django.urls import path
from rest_framework import routers

from tags.tags_api.viewsets import *
from warehouses.warehouses_api.viewsets import *
from users.users_api.viewsets import *

router = routers.DefaultRouter()

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
