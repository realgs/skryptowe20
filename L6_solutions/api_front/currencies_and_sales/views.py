import logging

import requests
from django.shortcuts import render
from json2html import json2html

logging.basicConfig(level=logging.DEBUG)

BASE_URL = "http://127.0.0.1:5000"


def index(request):
    return render(request, "index.html")


def get_table(endpoint):
    logging.info(f"Requesting data from {endpoint}")

    response = requests.get(endpoint)

    if response.status_code == 200:
        return json2html.convert(response.json(), table_attributes="class=\"table table-hover\"")
    else:
        return "<h1>No data found</>"


def rates_single_date(request):
    context = {
        'title': "USD rates",
        'heading': "USD rate for single date"
    }

    if request.method == "POST":
        date = request.POST.get("date")
        endpoint = f"{BASE_URL}/rates/usd/{date}"

        table_html = get_table(endpoint)
        context["table"] = table_html

    return render(request, "single_date.html", context=context)


def rates_date_range(request):
    context = {
        'title': "USD rates",
        'heading': "USD rates from date range"
    }

    if request.method == "POST":
        start = request.POST.get("start")
        end = request.POST.get("end")
        endpoint = f"{BASE_URL}/rates/usd/{start}/{end}"

        table_html = get_table(endpoint)
        context["table"] = table_html

    return render(request, "date_range.html", context=context)
