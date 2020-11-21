import datetime as dt
import requests
from datetime import date

API_URL = "http://api.nbp.pl/api/exchangerates/rates/"


def get_listing_coursers_between_date(currency, date_from_string, date_to_string):
    date_from = datetime_converter(date_from_string)
    date_to = datetime_converter(date_to_string)
    number_of_days = (date_from - date_to).days
    api_json_result = requests.get(API_URL + "a/" + str(currency) + "/" + str(date_from_string) + "/" + str(date_to_string)
                                   + "/?format=json").json()
    additional_content = {'number_of_days': number_of_days, 'date_from': date_from_string,
                          'date_to': date_to_string}
    api_json_result.update(additional_content)
    return api_json_result


def get_listing_courses(currency, number_of_days):
    return get_listing_coursers_between_date(currency, str(date.today() - dt.timedelta(number_of_days)), str(date.today()))


def get_rate_list(json):
    date_list = []
    mid_rate_list = []
    number_of_next_date = 0
    for data in json["rates"]:
        actual_date = datetime_converter(data["effectiveDate"])
        if len(date_list) != 0:
            next_date_object = date_list[len(date_list)-1] + dt.timedelta(days=1)
            while (next_date_object != actual_date) & (not number_of_next_date == json["number_of_days"]-1):
                date_list.append(next_date_object)
                mid_rate_list.append(mid_rate_list[len(mid_rate_list) - 1])
                next_date_object += dt.timedelta(days=1)
                number_of_next_date += 1
        else:
            date_before = datetime_converter(json["date_from"])
            while date_before < actual_date:
                date_list.append(date_before)
                mid_rate_list.append(data["mid"])
                date_before += dt.timedelta(days=1)
                number_of_next_date += 1
        date_list.append(actual_date)
        mid_rate_list.append(data["mid"])
        number_of_next_date += 1
    return date_list, mid_rate_list


def datetime_converter(string_date):
    return dt.datetime.strptime(str(string_date), '%Y-%m-%d')
