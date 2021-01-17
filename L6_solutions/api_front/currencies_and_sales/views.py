import logging

import pandas as pd
import requests
from django.shortcuts import render
from json2html import json2html

logging.basicConfig(level=logging.DEBUG)

BASE_URL = "http://127.0.0.1:5000"
BASE_URL_SALES = f"{BASE_URL}/sales"
BASE_URL_RATES = f"{BASE_URL}/rates/usd"
DATE_START = "2013-01-01"
DATE_END = "2014-12-31"

CCY_COLORS = {'PLN': 'grey', 'USD': 'blue'}


def get_endpoint(request, root_url, date_range=False):
    start = request.POST.get("start")

    if date_range:
        end = request.POST.get("end")
        return f"{root_url}/{start}/{end}", start, end
    return f"{root_url}/{start}", start


def get_error_msg(status_code):
    if status_code == 404:
        return f"No data found. Note that data is available only for date range {DATE_START} - {DATE_END}"
    if status_code == 400:
        return "End date cannot be earlier than start date."
    return "Unknown error occurred"


def get_html_table(data):
    return json2html.convert(data, table_attributes="class=\"table table-hover\"")


def get_data(endpoint):
    logging.info(f"Requesting data from {endpoint}")

    response = requests.get(endpoint)
    logging.info(response.status_code)
    if response.status_code == 200:
        return response.json()
    else:
        return response.status_code


def get_sales_data_subset(data, currencies):
    df_columns = currencies
    df_columns.append('DATE')
    df_columns.reverse()
    data_subset = pd.DataFrame(data)[df_columns]

    return data_subset


def index(request):
    return render(request, "index.html")


def rates_single_date(request):
    context = {
        'title': "USD rates",
        'heading': "USD rate for single date"
    }

    if request.method == "POST":
        endpoint, desired_date = get_endpoint(request, BASE_URL_RATES)

        data = get_data(endpoint)
        if not type(data) is int:
            context["table"] = get_html_table(data)
            context["table_heading"] = f"USD rate from {desired_date}"
        else:
            context["error_msg"] = get_error_msg(data)

    return render(request, "single_date.html", context=context)


def rates_date_range(request):
    context = {
        'title': "USD rates",
        'heading': "USD rates from date range",
    }

    if request.method == "POST":
        endpoint, start_date, end_date = get_endpoint(request, BASE_URL_RATES, date_range=True)

        data = get_data(endpoint)
        if not type(data) is int:
            context["table"] = get_html_table(data)
            context["datasets"] = [
                {"label": "USD rate", "data": pd.DataFrame(data)['USD'].to_list(), "color": CCY_COLORS['USD']}]
            context["labels"] = pd.DataFrame(data)['effectiveDate'].to_list()
            context["table_heading"] = f"USD rates from {start_date} to {end_date}"

        else:
            context["error_msg"] = get_error_msg(data)

    return render(request, "date_range.html", context=context)


def sales_single_date(request):
    context = {
        'title': "Sales",
        'heading': "Single date sales",
        'available_currencies': ['USD', 'PLN']

    }

    if request.method == "POST":
        endpoint, desired_date = get_endpoint(request, BASE_URL_SALES)
        currencies = request.POST.getlist("ccy")

        data = get_data(endpoint)
        if not type(data) is int:
            table_data = get_sales_data_subset(data, currencies.copy())
            context["table"] = get_html_table(table_data.to_json(orient="records"))
            context["table_heading"] = f"Sales from {desired_date}"

        else:
            context["error_msg"] = get_error_msg(data)

    return render(request, "single_date.html", context=context)


def sales_date_range(request):
    context = {
        'title': "Sales",
        'heading': "Sales from date range",
        'available_currencies': ['USD', 'PLN']
    }
    if request.method == "POST":
        endpoint, start_date, end_date = get_endpoint(request, BASE_URL_SALES, date_range=True)
        currencies = request.POST.getlist("ccy")

        data = get_data(endpoint)
        if not type(data) is int:
            table_data = get_sales_data_subset(data, currencies.copy())
            context["table"] = get_html_table(table_data.to_json(orient="records"))
            context["datasets"] = []
            for ccy in currencies:
                # noinspection PyTypeChecker
                context["datasets"].append(
                    {
                        "label": f"Sales in {ccy}",
                        "data": table_data[ccy].to_list(),
                        "color": CCY_COLORS[ccy]})
            logging.info(context["datasets"])
            context["labels"] = table_data['DATE'].to_list()
            context["table_heading"] = f"Sales from {start_date} to {end_date}"

        else:
            context["error_msg"] = get_error_msg(data)

    return render(request, "date_range.html", context=context)
