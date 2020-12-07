from django.urls import path

from .views import ManageView

urlpatterns =[
    path('', ManageView.as_view(), name='manage'),
]
