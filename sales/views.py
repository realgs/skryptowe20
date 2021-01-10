from sales.models import Currency, SalesStats
from rest_framework import viewsets
from rest_framework import permissions
from sales.serializers import CurrencySerializer, SalesStatsSerializer
from datetime import datetime
from rest_framework.exceptions import ValidationError

import constants


class CurrencyRangeList(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        symbol = self.request.query_params.get('symbol', "USD")
        start = self.request.query_params.get('start', datetime.strftime(constants.FIRST_DAY, '%Y-%m-%d'))
        end = self.request.query_params.get('end', datetime.strftime(constants.LAST_DAY, '%Y-%m-%d'))
        if datetime.strptime(start, '%Y-%m-%d') < constants.FIRST_DAY \
                or datetime.strptime(end, '%Y-%m-%d') > constants.LAST_DAY:
            raise ValidationError({"error": ["Dates are not is valid range"]})
        if symbol not in constants.Currency._value2member_map_:
            raise ValidationError({"error": [f"{symbol} is not valid currency symbol"]})
        qs = qs.filter(symbol=symbol, date__range=(start, end))

        return qs


class SalesStatGetView(viewsets.ReadOnlyModelViewSet):
    queryset = SalesStats.objects.all()
    serializer_class = SalesStatsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        symbol = self.request.query_params.get('symbol', "PLN")
        start = self.request.query_params.get('start', datetime.strftime(constants.FIRST_DAY_SALES, '%Y-%m-%d'))
        end = self.request.query_params.get('end', datetime.strftime(constants.LAST_DAY_SALES, '%Y-%m-%d'))
        if datetime.strptime(start, '%Y-%m-%d') < constants.FIRST_DAY_SALES \
                or datetime.strptime(end, '%Y-%m-%d') > constants.LAST_DAY_SALES:
            raise ValidationError({"error": ["Dates are not is valid range"]})

        qs = qs.values('date', 'sales_sum')
        qs = qs.filter(date__range=(start, end))

        if symbol == "PLN":
            return qs
        else:
            currencySet = Currency.objects.filter(symbol=symbol, date__range=(start, end)).values()

            j = 0
            for sale in qs:
                while currencySet[j]["date"] != sale["date"]:
                    j += 1
                sale["sales_sum"] /= currencySet[j]["value"]

        return qs
