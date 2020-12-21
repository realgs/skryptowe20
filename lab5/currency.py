import datetime as dt
import requests
from datetime import date

API_URL = "http://api.nbp.pl/api/exchangerates/rates/"
API_DAY_LIMIT = 365


def get_listing_coursers_between_date(currency, date_from_string, date_to_string):
    date_from = __datetime_converter(date_from_string)
    date_to = __datetime_converter(date_to_string)
    number_of_days = (date_to - date_from).days
    nb_days_remaining_to_download = number_of_days
    add_content = []
    while nb_days_remaining_to_download != 0:
        if nb_days_remaining_to_download > API_DAY_LIMIT:
            date_from_object = date_from + dt.timedelta(days=(number_of_days - nb_days_remaining_to_download))
            date_to_object = date_from_object + dt.timedelta(days=API_DAY_LIMIT)
            api_json_result_add = get_listing_coursers_less_than_year(currency, str(date_from_object)[:10],
                                                                      str(date_to_object)[:10])
            nb_days_remaining_to_download -= API_DAY_LIMIT
        else:
            date_from_object = date_from + dt.timedelta(days=(number_of_days - nb_days_remaining_to_download) + 1)
            api_json_result_add = get_listing_coursers_less_than_year(currency, str(date_from_object)[:10],
                                                                      date_to_string)
            nb_days_remaining_to_download = 0
        add_content += __add_json_row_to_list(api_json_result_add["rates"])
    api_json_result = {'rates': add_content, 'number_of_days': number_of_days, 'date_from': date_from_string,
                       'date_to': date_to_string}
    return api_json_result


def get_listing_coursers_less_than_year(currency, date_from_string, date_to_string):
    api_json_result = requests.get(
        f"{API_URL}a/{str(currency)}/{str(date_from_string)}/{str(date_to_string)}/?format=json").json()
    return api_json_result


def get_listing_courses(currency, number_of_days):
    return get_listing_coursers_between_date(currency, str(date.today() - dt.timedelta(number_of_days)),
                                             str(date.today()))


def get_one_day_currency_rate(currency_id, date):
    api_json_result = ""
    date += " 00:00:00"
    is_interpolated = False
    while api_json_result == "":
        try:
            api_json_result = requests.get(f"{API_URL}a/{str(currency_id)}/{str(date)[:10]}/?format=json").json()
        except ValueError:
            date = dt.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S') - dt.timedelta(days=1)
            is_interpolated = True
    return api_json_result["rates"][0]["mid"], is_interpolated



def get_rate_list(json):
    currency_data = []
    number_of_next_date = 0
    for data in json["rates"]:
        actual_date = __datetime_converter(data["effectiveDate"])
        if len(currency_data) != 0:
            next_date_object = __datetime_with_time_converter(currency_data[len(currency_data) - 1]["date"]) + \
                               dt.timedelta(days=1)
            while (next_date_object != actual_date) & (not number_of_next_date == json["number_of_days"]):
                currency_data.append({"date": f'{next_date_object}',
                                      "mid_rate": currency_data[len(currency_data) - 1]["mid_rate"],
                                      "interpolated": True})
                next_date_object += dt.timedelta(days=1)
                number_of_next_date += 1
        else:
            date_before = __datetime_converter(json["date_from"])
            while (date_before < actual_date) & (not number_of_next_date == json["number_of_days"]):
                currency_data.append({"date": f'{date_before}', "mid_rate": data["mid"],
                                      "interpolated": True})
                date_before += dt.timedelta(days=1)
                number_of_next_date += 1
        currency_data.append({"date": f'{actual_date}', "mid_rate": data["mid"],
                              "interpolated": False})
        number_of_next_date += 1
    if number_of_next_date != json["number_of_days"] + 1:
        next_date_object = __datetime_with_time_converter(currency_data[len(currency_data) - 1]["date"]) + dt.timedelta(
            days=1)
        while (next_date_object <= __datetime_converter(json["date_to"])) & \
                (not number_of_next_date == json["number_of_days"]):
            currency_data.append({"date": f'{next_date_object}',
                                  "mid_rate": currency_data[len(currency_data) - 1]["mid_rate"],
                                  "interpolated": True})
            next_date_object += dt.timedelta(days=1)
            number_of_next_date += 1
        currency_data.append({"date": f'{next_date_object}', "mid_rate": data["mid"],
                              "interpolated": False})
        number_of_next_date += 1

    return currency_data


def __datetime_converter(string_date):
    return dt.datetime.strptime(str(string_date), '%Y-%m-%d')


def __datetime_with_time_converter(string_datetime):
    return dt.datetime.strptime(str(string_datetime), '%Y-%m-%d %H:%M:%S')


def __add_json_row_to_list(json):
    new_list = []
    for row in json:
        new_list.append(row)
    return new_list
