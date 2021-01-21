from django.urls import path, register_converter
from .views import exchange_rates_list, exchange_rates_list_date_filtered
from datetime import datetime


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, val):
        return datetime.strptime(val, '%Y-%m-%d')

    def to_url(self, val):
        return val


register_converter(DateConverter, 'date')

urlpatterns = [
    path('rates/', exchange_rates_list),
    path('rates/<date:date_from>/<date:date_to>', exchange_rates_list_date_filtered),
]
