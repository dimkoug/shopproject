from django.contrib import admin

from .models import Order, OrderDetail, OrderStatus
from .forms import OrderForm, OrderDetailForm

class OrderAdmin(admin.ModelAdmin):
    model = Order
    form = OrderForm

class OrderDetailAdmin(admin.ModelAdmin):
    model = OrderDetail
    form = OrderDetailForm

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
admin.site.register(OrderStatus, admin.ModelAdmin)
