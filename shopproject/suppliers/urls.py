from django.urls import path

from core.patterns import get_patterns

from .functions import (
    get_suppliers_for_sb,
)


app_name = 'suppliers'
urlpatterns = [
    #path('', IndexView.as_view(), name="index"),
    path('sb/', get_suppliers_for_sb, name='sb-suppliers'),
]
