import datetime as dt
import requests
from datetime import date, timedelta
import json


API_URL = "http://api.nbp.pl/api/exchangerates/rates/"


def get_listing_courses(currency, number_of_days):
    date_from = date.today() - dt.timedelta(number_of_days)
    date_to = dt.date.today()
    x = requests.get(API_URL + "a/" + str(currency) + "/" + str(date_from) + "/" + str(date_to) + "/?format=json").json()
    y = {'number_of_days': number_of_days, 'date_from': datetime_konwerter(str(date_from)),
         'date_to': datetime_konwerter(str(date_to))}
    x.update(y)
    return x


def get_tablice_kursow(json):
    date = []
    mid = []
    kolejna_data = 0
    for data in json["rates"]:
        actual_date = datetime_konwerter(data["effectiveDate"])
        if len(date) != 0:
            next_date_object = date[len(date)-1] + dt.timedelta(days=1)
            while (next_date_object != actual_date) & (not kolejna_data == json["number_of_days"]-1):
                date.append(next_date_object)
                mid.append(mid[len(mid) - 1])
                next_date_object += dt.timedelta(days=1)
                kolejna_data += 1
        else:
            date_before = json["date_from"]
            while date_before < actual_date:
                date.append(date_before)
                mid.append(data["mid"])
                date_before += dt.timedelta(days=1)
                kolejna_data += 1
        date.append(actual_date)
        mid.append(data["mid"])
        kolejna_data += 1

    return date, mid


def datetime_konwerter(date):
    return dt.datetime.strptime(date, '%Y-%m-%d')
