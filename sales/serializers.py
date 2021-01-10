from sales.models import SalesStats, Currency
from rest_framework import serializers
import constants


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['symbol', 'date', 'value', 'interpolated']


class SalesStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesStats
        fields = ['date', 'sales_sum']
        # for c in constants.Currency:
        #     fields.append(c.value.lower())
