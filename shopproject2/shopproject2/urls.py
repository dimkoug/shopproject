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


from .views import HomeView, ManageView

from rest_framework.authtoken import views as api_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('manage/', ManageView.as_view(), name='manage'),
    path('users/', include('users.urls')),
    path('profiles/', include('profiles.urls')),
    path('products/', include('products.urls')),
    path('api-token-auth/', api_views.obtain_auth_token, name='api-token'),
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
