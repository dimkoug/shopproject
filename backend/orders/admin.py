from django.contrib import admin

# Register your models here.

from .models import Order, OrderItem
from .forms import OrderForm,OrderItemForm, OrderItemFormSet


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    formset = OrderItemFormSet
    fk_name = 'order'


class OrderAdmin(admin.ModelAdmin):
    model = Order
    form = OrderForm

    inlines = [
        OrderItemInline,
    ]


admin.site.register(Order, OrderAdmin)