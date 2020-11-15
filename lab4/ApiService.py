import requests
from datetime import date, timedelta

from Exceptions.ApiError import ApiError


class AverageExchangeRate:
    def __init__(self, currencyCode, mid, dateStr):
        self.currencyCode = currencyCode
        self.mid = mid
        dateStrSplited = dateStr.split("-")
        self.effectiveDate = date(int(dateStrSplited[0]), int(dateStrSplited[1]), int(dateStrSplited[2]))


def getAverageExchangeRatesInDays(currencyCode, days):
    resp = __getCurrencyFromOneTableInDays__("a", currencyCode, days)

    if resp.status_code != 200:
        if resp.status_code == 400:
            raise ApiError("Invalid days param")

        resp = __getCurrencyFromOneTableInDays__("b", currencyCode, days)
        if resp.status_code != 200:
            raise ApiError("No data found")

    returnData = []
    for item in resp.json()["rates"]:
        returnData.append(AverageExchangeRate(currencyCode, item["mid"], item["effectiveDate"]))
    return returnData


def __getCurrencyFromOneTableInDays__(tableCode, currencyCode, days):
    startDate = date.today() - timedelta(days=days)

    url = "http://api.nbp.pl/api/exchangerates/rates/"
    paramsUrl = "/{}/{}/{}".format(currencyCode, startDate, date.today())
    return requests.get(url + tableCode + paramsUrl)


def getUsdAndEurOverHalfOfYear():
    return getAverageExchangeRatesInDays("USD", 182), getAverageExchangeRatesInDays("EUR", 182)
