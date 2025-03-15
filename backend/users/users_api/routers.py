from django.urls import include, path
from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register(r'users', viewsets.UserViewSet)
router.register(r'groups', viewsets.GroupViewSet)

urlpatterns = router.urls + [
    path('login/', viewsets.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('current_user/', viewsets.current_user),
    path('register/', viewsets.RegisterApi.as_view()),
    # path('users/', UserList.as_view())
]
