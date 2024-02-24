"""shopproject2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from core.functions import delete_model

from .views import TestView
from shop.views import IndexView
from core.functions import get_sb_data


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', include('haystack.urls')),
    path('test/', TestView.as_view(), name='test'),
    path('sb_data/', get_sb_data, name='sb-data'),
    path('delete/', delete_model, name='delete'),
    path('cms/', include('cms.urls', namespace='cms')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('brands/', include('brands.urls', namespace='brands')),
    path('tags/', include('tags.urls', namespace='tags')),
    path('api/', include('shop.shopapi.routers')),
    path('users/', include('users.urls')),
    path('users/api/', include('users.api.routers')),
    path('profiles/', include('profiles.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api-token-auth/', obtain_jwt_token),
    # path('api-token-refresh/', refresh_jwt_token),
    #path('api-token-verify/', verify_jwt_token),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
        urlpatterns += [
            path('__debug__', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
