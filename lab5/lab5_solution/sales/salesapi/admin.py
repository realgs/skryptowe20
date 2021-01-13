from django.contrib import admin

from .models import *

admin.site.register(CurrencyRecord)
admin.site.register(DailySales)
admin.site.register(SalesOrders)