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

def getJsonRate(request, one_date):
    if isBelowTimeLimit(request):
        try:
            response = CurrencyRecord.objects.get(effectivedate=one_date)
        except CurrencyRecord.DoesNotExist:
            return JsonResponse({"unrecognized_url": 1})

        return JsonResponse({one_date: response.currencyvalue})
    else:
        return HttpResponse(status=404)

def getJsonRateTwoDates(request, from_date, to_date):
    if isBelowTimeLimit(request):
        response = {}
        missing_records=0
        try:
            from_object = CurrencyRecord.objects.get(effectivedate=from_date)
            to_object = CurrencyRecord.objects.get(effectivedate=to_date)
        except CurrencyRecord.DoesNotExist:
            return JsonResponse({"unrecognized_url": 1})

        if from_object.id > to_object.id:
            ids_range = range(to_object.id, from_object.id)
        else:
            ids_range = range(from_object.id, to_object.id)

        for i in ids_range:
            try:
                record = CurrencyRecord.objects.get(id=i)
                response[record.effectivedate]=record.currencyvalue
            except CurrencyRecord.DoesNotExist:
                missing_records+=1
                response["missing_records"]=missing_records
        return JsonResponse(response)
    else:
        return HttpResponse(status=404)
