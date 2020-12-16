from django.shortcuts import render
from django.http import HttpResponse
from rates.DataAPI.fetcher import get_avg_rates_for_currency

# Create your views here.
def test(request):
    return HttpResponse("Test tylko tutaj hehe")

def history(request, currency_code, start_date, end_date):
    wrapper = get_avg_rates_for_currency(currency_code, start_date, end_date)
    return HttpResponse(f"{wrapper}")