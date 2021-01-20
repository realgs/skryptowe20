import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests


# Create your views here.
def home(request):
    return render(request, "interface_app/home.html")


def request_builder(request):
    return show_exchange_rates(request, datetime.date(year=2009, month=2, day=2),
                               datetime.date(year=2009, month=5, day=24), 'USD')


def show_exchange_rates(request, start_date, end_date, currency_code):
    start_date_string = __format_date(start_date)
    end_date_string = __format_date(end_date)
    request_url = 'http://127.0.0.1:5000/api/exchangerate/{0}/{1}/{2}'.format(currency_code, start_date_string,
                                                                              end_date_string)
    response = requests.get(request_url)
    other_currency_code = 'PLN' if currency_code == 'USD' else 'USD'

    return render(request, "interface_app/display_exchange_rates.html",
                  context={'exchange_rates_json': response.json(),
                           'other_currency_code': other_currency_code,
                           'start_date': start_date_string,
                           'end_date': end_date_string,
                           })


def __format_date(date):
    return date.strftime('%Y-%m-%d')
