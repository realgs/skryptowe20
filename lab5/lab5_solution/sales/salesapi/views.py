from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponse
from datetime import datetime

from .serializers import *
from .models import *

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

        return JsonResponse({"date": one_date,
                             "value": response.currencyvalue, 
                             "isInterpolated": response.interpolated})
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
                response[record.effectivedate]={"value": record.currencyvalue, 
                             "isInterpolated": record.interpolated}
            except CurrencyRecord.DoesNotExist:
                missing_records+=1
                response["missing_records"]=missing_records
        return JsonResponse(response)
    else:
        return HttpResponse(status=404)

def getJsonSale(request, one_date):
    if isBelowTimeLimit(request):
        try:
            response = DailySales.objects.get(salesdate=one_date)
        except DailySales.DoesNotExist:
            return JsonResponse({"unrecognized_url": 1})

        return JsonResponse({"date": one_date,
                             "pln_sales": response.plnsales,
                             "usd_sales": response.usdsales})
    else:
        return HttpResponse(status=404)

def getJsonSaleTwoDates(request, from_date, to_date):
    if isBelowTimeLimit(request):
        response = {}
        missing_records=0

        try:
            from_object = DailySales.objects.get(salesdate=from_date)
            to_object = DailySales.objects.get(salesdate=to_date)
        except DailySales.DoesNotExist:
            return JsonResponse({"unrecognized_url": 1})

        if from_object.sales_id > to_object.sales_id:
            ids_range = range(to_object.sales_id, from_object.sales_id)
        else:
            ids_range = range(from_object.sales_id, to_object.sales_id)

        for i in ids_range:
            try:
                record = DailySales.objects.get(sales_id=i)
                response[record.salesdate]={"pln_sales": record.plnsales, "usd_sales": record.usdsales}
            except CurrencyRecord.DoesNotExist:
                missing_records+=1
                response["missing_records"]=missing_records
        return JsonResponse(response)
    else:
        return HttpResponse(status=404)

def isBelowTimeLimit(request):
    if request.user.is_authenticated:
        key = "requests_num_"+str(request.user.username)
    else:
        key = "requests_num_anon"

    try:
        requests_num = request.session[key]
    except KeyError:
        request.session[key] = {"last_request": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "sum": 0}
        requests_num = request.session[key]

    if requests_num["sum"] >= REQUESTS_PER_MINUTE \
        and (datetime.now() - datetime.strptime(requests_num["last_request"], "%Y-%m-%d %H:%M:%S")).seconds < 60:
            request.session.modified=True
            return False
    elif requests_num["sum"] >= REQUESTS_PER_MINUTE:
        requests_num["sum"]=0
    
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requests_num["last_request"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requests_num["sum"]+=1
    request.session.modified=True
    return True
