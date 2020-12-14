from django.shortcuts import render
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponse
from datetime import datetime

from .serializers import *
from .models import *


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = CurrencyRecord.objects.all().order_by('id')
    serializer_class = CurrencySerializer

class DailySalesViewSet(viewsets.ModelViewSet):
    queryset = DailySales.objects.all().order_by('sales_id')
    serializer_class = DailySalesSerializer

class CacheSales:
    def __init__(self):
        self.cached_values = {}
        self.init_date = datetime.now()

    def add(self, one_date, response):
        if (datetime.now() - self.init_date).seconds >= MAX_CACHE_TIME_SECONDS:
            self.cached_values = {}
            self.init_date = datetime.now()
        if len(self.cached_values.keys()) >= MAX_CACHE_LENGTH:
            first_key = list(self.cached_values.keys())[0]
            del self.cached_values[first_key]
        self.cached_values[one_date] = response

    def getResponse(self, one_date):
        if one_date in self.cached_values:
            return self.cached_values[one_date]
        else: return None

class CacheSalesRange:
    def __init__(self):
        self.cached_values = {}
        self.init_date = datetime.now()

    def add(self, from_date, to_date, response):
        if (datetime.now() - self.init_date).seconds >= MAX_CACHE_TIME_SECONDS:
            self.cached_values = {}
            self.init_date = datetime.now()
        if len(self.cached_values.keys()) >= MAX_CACHE_LENGTH:
            first_key = list(self.cached_values.keys())[0]
            del self.cached_values[first_key]
        new_key = from_date+"/"+to_date
        self.cached_values[new_key] = response

    def getResponse(self, from_date, to_date):
        new_key = from_date+"/"+to_date
        if new_key in self.cached_values:
            return self.cached_values[new_key]
        else: return None

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
        cached_response = CACHE_SALES.getResponse(one_date)
        if cached_response != None: return cached_response
        else:
            try:
                response = DailySales.objects.get(salesdate=one_date)
            except DailySales.DoesNotExist:
                return JsonResponse({"unrecognized_url": 1})

            json_response = JsonResponse({"date": one_date,
                                 "pln_sales": response.plnsales,
                                 "usd_sales": response.usdsales})
            CACHE_SALES.add(one_date, json_response)
            return json_response
    else:
        return HttpResponse(status=404)

def getJsonSaleTwoDates(request, from_date, to_date):
    if isBelowTimeLimit(request):
        cached_response = CACHE_SALES_RANGE.getResponse(from_date, to_date)
        if cached_response != None: return cached_response
        else:
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
            json_response = JsonResponse(response)
            CACHE_SALES_RANGE.add(from_date, to_date, json_response)
            return json_response
    else:
        return HttpResponse(status=404)

def isBelowTimeLimit(request):
    if request.user.is_authenticated:
        key = "requests_num_"+str(request.user.username)
    else:
        key = "requests_num_"+get_client_ip(request)
        print(key)

    try:
        requests_num = request.session[key]
        print(requests_num)
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

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

REQUESTS_PER_MINUTE = 50
MAX_CACHE_LENGTH = 100
MAX_CACHE_TIME_SECONDS = 10*60
CACHE_SALES = CacheSales()
CACHE_SALES_RANGE = CacheSalesRange()
