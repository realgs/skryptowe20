import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests


# Create your views here.
def home(request):
    return render(request, "interface_app/home.html")


def request_builder(request):
    if request.method == 'POST':
        if request.POST['select-value'] == 'exchange-rates':
            # użytkownik chce kurs walut
            if request.POST['select-date'] == 'date-range':
                start_date = request.POST['date-range-start']
                end_date = request.POST['date-range-end']
            else:
                start_date = end_date = request.POST['single-date-input']
            return show_exchange_rates(request, start_date, end_date, request.POST['currencies'], True)
        else:
            # użytkownik chce podsumowanie sprzedaży
            if request.POST['select-date'] == 'date-range':
                start_date = request.POST['date-range-start']
                end_date = request.POST['date-range-end']
            else:
                start_date = end_date = request.POST['single-date-input']
            return show_sales(request, start_date, end_date)

    return render(request, "interface_app/request_builder.html")


def show_exchange_rates(request, start_date, end_date, currency_code, is_chart):
    request_url = 'http://127.0.0.1:5000/api/exchangerate/{0}/{1}/{2}'.format(currency_code, start_date,
                                                                              end_date)
    response = requests.get(request_url)
    other_currency_code = 'PLN' if currency_code == 'USD' else 'USD'

    if is_chart:
        template_name = "interface_app/display_exchange_rates_chart.html"
    else:
        template_name = "interface_app/display_exchange_rates.html"

    return render(request, template_name,
                  context={'exchange_rates_json': response.json(),
                           'other_currency_code': other_currency_code,
                           'start_date': start_date,
                           'end_date': end_date,
                           })


def show_sales(request, start_date, end_date):
    request_url = 'http://127.0.0.1:5000/api/sales/{0}/{1}/'.format(start_date, end_date)
    response = requests.get(request_url)
    return render(request, "interface_app/display_sales.html",
                  context={'sales_json': response.json(),
                           'start_date': start_date,
                           'end_date': end_date
                           })
