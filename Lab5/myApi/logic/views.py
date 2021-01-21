from django.shortcuts import render
from sqlite3 import OperationalError
from django.http import HttpResponse, HttpResponseNotFound
from logic.DataAPI.fetcher import get_avg_rates_for_currency
from logic.DataAPI.database_operations import get_summary
from logic.DataAPI.exceptions import IncorrectDateException, UnsupportedCurrencyException, FetchFailException
from logic.limiter import can_request

def history(request, currency_code, start_date, end_date):
    if not can_request():
        return HttpResponseNotFound("{"
                '"error":"Requests limit reached"'
                "}")
    try:
        wrapper = get_avg_rates_for_currency(currency_code, start_date, end_date)
    except IncorrectDateException:
        return HttpResponseNotFound("{"
                       '"error":"Incorrect date"'
                       "}")
    except UnsupportedCurrencyException:
        return HttpResponseNotFound("{"
                       '"error":"Unsupported currency"'
                       "}")
    except FetchFailException:
        return HttpResponseNotFound("{"
                       '"error":"Failed to fetch from NBPAPI"'
                       "}")
    except ValueError:
        return HttpResponseNotFound("{"
                       '"error":"Incorrect input"'
                       "}")
    except IndexError:
        return HttpResponseNotFound("{"
                       '"error":"Start date should be smaller than end date"'
                       "}")
    return HttpResponse(f"{wrapper}")

def summary(request, currency_code, date):
    if not can_request():
        return HttpResponseNotFound("{"
                '"error":"Requests limit reached"'
                "}")
    try:
        summary = get_summary(currency_code, date)
        print(f"TEST: {currency_code}, {date}, {summary}")
    except OperationalError:
        return HttpResponseNotFound("{"
                       '"error":"Internal database error"'
                       "}")
    except IncorrectDateException:
        return HttpResponseNotFound("{"
                       '"error":"Incorrect date"'
                       "}")
    except UnsupportedCurrencyException:
        return HttpResponseNotFound("{"
                       '"error":"Unsupported currency"'
                       "}")
    return HttpResponse(f"{summary}")
