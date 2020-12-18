from sales.models import SalesStats, Currency
from rest_framework import serializers


class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Currency
        fields = ['symbol', 'date', 'value', 'interpolated']


class SalesStatsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SalesStats
        fields = ['date', 'sales_sum', 'usd', 'eur']
