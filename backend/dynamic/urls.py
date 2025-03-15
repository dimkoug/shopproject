from django.urls import path


from dynamic import views


urlpatterns = [
    path('<str:app_name>/<str:model_name>/',views.DynamicListView.as_view(),name='dynamic_list'),
    path('add/<str:app_name>/<str:model_name>/',views.DynamicCreateView.as_view(),name='dynamic_add'),
    path('view/<str:app_name>/<str:model_name>/<int:pk>/',views.DynamicDetailView.as_view(),name='dynamic_view'),
    path('change/<str:app_name>/<str:model_name>/<int:pk>/',views.DynamicUpdateView.as_view(),name='dynamic_change'),
    path('delete/<str:app_name>/<str:model_name>/<int:pk>/',views.DynamicDeleteView.as_view(),name='dynamic_delete'),
]


