from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponse
from datetime import datetime

from .serializers import *
from .models import *
# Create your views here.

REQUESTS_PER_MINUTE = 10

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = CurrencyRecord.objects.all().order_by('id')
    serializer_class = CurrencySerializer

class DailySalesViewSet(viewsets.ModelViewSet):
    queryset = DailySales.objects.all().order_by('sales_id')
    serializer_class = DailySalesSerializer