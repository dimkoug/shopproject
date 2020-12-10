from django.urls import path

from .views import (
    ManageView,
    CategoryListView,
    CategoryDetailView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView

)

app_name='cms'
urlpatterns =[
    path('', ManageView.as_view(), name='manage'),
    path('category/list/', CategoryListView.as_view(),
         name='category-list'),
    path('category/create/', CategoryCreateView.as_view(),
         name='category-create'),
    path('category/<int:pk>/detail/', CategoryDetailView.as_view(),
         name='category-detail'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(),
         name='category-update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(),
         name='category-delete'),
]
