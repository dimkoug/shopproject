from django.urls import path, include


from heroes.views import *

app_name = 'heroes'

urlpatterns = [
    path('',
         HeroListView.as_view(), name='hero_list'),
    path('add/',
         HeroCreateView.as_view(), name='hero_add'),
    path('view/<int:pk>/',
         HeroDetailView.as_view(), name='hero_view'),
    path('change/<int:pk>/',
         HeroUpdateView.as_view(), name='hero_change'),
    path('delete/<int:pk>/',
         HeroDeleteView.as_view(), name='hero_delete'),
     
     path("add/heroitem/<int:hero_id>/",add_hero_item,name='add_heroitem'),

     path("delete/heroitem/<int:hero_id>/<int:id>/",delete_hero_item,name='delete_heroitem'),

    path('api/',include('heroes.heroes_api.routers')),
]
