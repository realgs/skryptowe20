from sales.models import Currency, SalesStats
from rest_framework import viewsets
from rest_framework import permissions
from sales.serializers import CurrencySerializer, SalesStatsSerializer

class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SalesStats.objects.all().order_by('date')
    serializer_class = SalesStatsSerializer
    permission_classes = [permissions.IsAuthenticated]


class SalesStatsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]
