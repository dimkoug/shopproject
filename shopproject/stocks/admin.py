from django.contrib import admin

# Register your models here.
from .models import Stock
from .forms import StockForm

class StockAdmin(admin.ModelAdmin):
    model = Stock
    form = StockForm


admin.site.register(Stock, StockAdmin)