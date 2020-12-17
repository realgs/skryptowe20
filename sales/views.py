from sales.models import Currency, SalesStats
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from sales.serializers import CurrencySerializer, SalesStatsSerializer
from datetime import datetime
from django.http import JsonResponse
from datetime import datetime
from django.http import Http404


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Currency.objects.all().order_by('date')
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]


class SalesStatsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SalesStats.objects.all()
    serializer_class = SalesStatsSerializer
    permission_classes = [permissions.IsAuthenticated]


class CurrencyRangeList(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        symbol = self.request.query_params.get('symbol')
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', datetime.now())
        if datetime.strptime(start, '%Y-%m-%d') < datetime.strptime('2001-01-02', '%Y-%m-%d') \
                or datetime.strptime(end, '%Y-%m-%d') > datetime.strptime('2020-01-02', '%Y-%m-%d') \
                or symbol not in ['USD', 'EUR']:
            raise Http404()

        if symbol is not None:
            qs = qs.filter(symbol=symbol, date__range=(start, end))
        return qs
