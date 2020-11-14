import requests
from datetime import date, timedelta

from Exceptions.ApiError import ApiError


def getAverageExchangeRatesInDays(currencyCode, days):
    startDate = date.today() - timedelta(days=days)

    url = "http://api.nbp.pl/api/exchangerates/rates/"
    paramsUrl = "/{}/{}/{}".format(currencyCode, startDate, date.today())
    resp = requests.get(url + "a" + paramsUrl)

    if resp.status_code != 200:
        if resp.status_code == 400:
            raise ApiError("Invalid days param")

        resp = requests.get(url + "b" + paramsUrl)
        if resp.status_code != 200:
            raise ApiError("No data found")

    returnData = []
    for item in resp.json()["rates"]:
        returnData.append(item)

    return returnData


