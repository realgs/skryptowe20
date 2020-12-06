from rest_framework import serializers
from .models import *

class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurrencyRecord
        fields = ('id', 'effectivedate', 'currencyvalue')

class DailySalesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DailySales
        fields = ('sales_id', 'salesdate', 'plnsales', 'usdsales')

class SalesOrdersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CurrencyRecord
        fields = ('orderid', 'orderdate', 'totaldue')
        