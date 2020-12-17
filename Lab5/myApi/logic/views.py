from django.shortcuts import render
from django.http import HttpResponse
from logic.DataAPI.fetcher import get_avg_rates_for_currency
from logic.DataAPI.database_operations import get_summary

def history(request, currency_code, start_date, end_date):
    wrapper = get_avg_rates_for_currency(currency_code, start_date, end_date)
    return HttpResponse(f"{wrapper}")

def summary(request, currency_code, date):
    summary = get_summary(currency_code, date)
    return HttpResponse(f"{summary}")
