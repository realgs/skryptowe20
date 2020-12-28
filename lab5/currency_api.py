import requests as req
from datetime import timedelta
import datetime as dt
import data_file as df


def get_elem(url):
    result = req.get(url)
    return result.json()


def get_currency_rates_by_dates(currency, date_from_str, date_to_str):
    date_from = __convert_to_date(date_from_str)
    date_to_help = __convert_to_date(date_to_str)
    number_of_days = (date_to_help - date_from).days
    if number_of_days > df.MAX_DAYS_AMOUNT:
        date_to = date_from + timedelta(days=df.MAX_DAYS_AMOUNT)
    else:
        date_to = date_to_help

    rates = []
    while date_to <= date_to_help:
        url = f'{df.NBP_API_URL}/a/{str(currency)}/{str(date_from)[:10]}/{str(date_to)[:10]}/?format=json'
        request = get_elem(url)
        rates += __json_to_list(request['rates'])
        date_from = date_to + timedelta(days=1)
        date_to = date_from + timedelta(days=df.MAX_DAYS_AMOUNT)

        if date_to > date_to_help > date_from:
            date_to = date_to_help

    result = {'rates': rates, 'days': number_of_days, 'date_from': date_from_str, 'date_to': date_to}
    return result


def get_currency_rates_list(json):
    currency_rate_data = []
    next_date_number = 0
    for rate in json["rates"]:
        actual_date = __convert_to_date(rate["effectiveDate"])

        if len(currency_rate_data) != 0:
            next_date = __convert_to_date(currency_rate_data[len(currency_rate_data) - 1]["date"][:10]) + \
                        dt.timedelta(days=1)
            while (next_date != actual_date) & (not next_date_number == json["days"]):
                currency_rate_data.append({"date": f'{next_date}',
                                           "mid": currency_rate_data[len(currency_rate_data) - 1]["mid"],
                                           "interpolated": True})
                next_date += dt.timedelta(days=1)
                next_date_number += 1
        else:
            previous_date = __convert_to_date(json["date_from"])
            while (previous_date < actual_date) & (not next_date_number == json["days"]):
                currency_rate_data.append({"date": f'{previous_date}',
                                           "mid": rate["mid"],
                                           "interpolated": True})
                previous_date += dt.timedelta(days=1)
                next_date_number += 1
        currency_rate_data.append({"date": f'{actual_date}',
                                   "mid": rate["mid"],
                                   "interpolated": False})
        next_date_number += 1

    if next_date_number != json["days"] + 1:
        next_date = __convert_to_date(currency_rate_data[len(currency_rate_data) - 1]["date"][:10]) + dt.timedelta(
            days=1)
        while (next_date <= __convert_to_date(json["date_to"])) & (not next_date_number == json["number_of_days"]):
            currency_rate_data.append({"date": f'{next_date}',
                                       "mid": currency_rate_data[len(currency_rate_data) - 1]["mid"],
                                       "interpolated": True})
            next_date += dt.timedelta(days=1)
            next_date_number += 1

        currency_rate_data.append({"date": f'{next_date}',
                                   "mid": rate["mid"],
                                   "interpolated": False})
        next_date_number += 1

    return currency_rate_data


def get_one_day_currency_rate(currency, date):
    api_json_result = ""
    date += " 00:00:00"
    interpolated = False
    while api_json_result == "":
        try:
            api_json_result = req.get(f"{df.NBP_API_URL}a/{str(currency)}/{str(date)[:10]}/?format=json").json()
        except ValueError:
            date = dt.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S') - dt.timedelta(days=1)
            interpolated = True
    return api_json_result["rates"][0]["mid"], interpolated


def __convert_to_date(date):
    return dt.datetime.strptime(str(date), '%Y-%m-%d')


def __json_to_list(json):
    new_list = []
    for row in json:
        new_list.append(row)
    return new_list
