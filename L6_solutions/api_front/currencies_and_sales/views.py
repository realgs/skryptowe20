import logging

import pandas as pd
import requests
from django.shortcuts import render
from json2html import json2html

logging.basicConfig(level=logging.DEBUG)

BASE_URL = "http://127.0.0.1:5000"


def index(request):
    return render(request, "index.html")


def get_table(data_json):
    return json2html.convert(data_json, table_attributes="class=\"table table-hover\"")


def get_json(endpoint):
    logging.info(f"Requesting data from {endpoint}")

    response = requests.get(endpoint)

    if response.status_code == 200:
        return response.json()


def rates_single_date(request):
    context = {
        'title': "USD rates",
        'heading': "USD rate for single date"
    }

    if request.method == "POST":
        date = request.POST.get("date")
        endpoint = f"{BASE_URL}/rates/usd/{date}"

        data_json = get_json(endpoint)
        if data_json:
            context["table"] = get_table(data_json)

    return render(request, "single_date.html", context=context)


def rates_date_range(request):
    context = {
        'title': "USD rates",
        'heading': "USD rates from date range",
    }

    if request.method == "POST":
        start = request.POST.get("start")
        end = request.POST.get("end")
        endpoint = f"{BASE_URL}/rates/usd/{start}/{end}"

        data_json = get_json(endpoint)
        if data_json:
            context["table"] = get_table(data_json)
            context["label"] = "USD rate"
            context["data"] = pd.DataFrame(data_json)['USD'].to_list()
            context["labels"] = pd.DataFrame(data_json)['effectiveDate'].to_list()

    return render(request, "date_range.html", context=context)


def sales_single_date(request):
    context = {
        'title': "Sales",
        'heading': "Single date sales",
    }

    if request.method == "POST":
        date = request.POST.get("date")
        endpoint = f"{BASE_URL}/sales/{date}"

        data_json = get_json(endpoint)
        if data_json:
            context["table"] = get_table(data_json)

    return render(request, "single_date.html", context=context)


def sales_date_range(request):
    context = {
        'title': "Sales",
        'heading': "Sales from date range",
        'available_currencies': ['USD', 'PLN']
    }
    if request.method == "POST":
        start = request.POST.get("start")
        end = request.POST.get("end")
        ccy = request.POST.get("ccy")
        logging.debug(ccy)
        endpoint = f"{BASE_URL}/sales/{start}/{end}"

        data_json = get_json(endpoint)
        if data_json:
            context["table"] = get_table(data_json)
            context["label"] = f"Sales in {ccy}"
            context["data"] = pd.DataFrame(data_json)[ccy].to_list()
            context["labels"] = pd.DataFrame(data_json)['DATE'].to_list()

    return render(request, "date_range.html", context=context)
