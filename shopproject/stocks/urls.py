from django.urls import path, include


app_name = 'stocks'

urlpatterns = [
    path('api/',include('stocks.stocks_api.routers')),
]
