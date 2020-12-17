import requests
from datetime import date, timedelta

from Exceptions.ApiError import ApiError


class AverageExchangeRate:
    def __init__(self, currencyCode, mid, dateStr):
        self.currencyCode = currencyCode
        self.mid = mid
        dateStrSplited = dateStr.split("-")
        self.effectiveDate = date(int(dateStrSplited[0]), int(dateStrSplited[1]), int(dateStrSplited[2]))


def getAverageExchangeRatesInDays(currencyCode, days, endDate=date.today()):
    days -= 1
    returnData = []
    if days > 366:
        returnData += getAverageExchangeRatesInDays(currencyCode, days - 366, endDate - timedelta(days=367))
        days = 366

    resp = __getCurrencyFromOneTableInDays__("a", currencyCode, days, endDate)

    if resp.status_code != 200:

        resp = __getCurrencyFromOneTableInDays__("b", currencyCode, days, endDate)
        if resp.status_code != 200:
            raise ApiError("No data found")

    for item in resp.json()["rates"]:
        returnData.append(AverageExchangeRate(currencyCode, item["mid"], item["effectiveDate"]))
    return returnData


def __getCurrencyFromOneTableInDays__(tableCode, currencyCode, days, endDate):
    url = "http://api.nbp.pl/api/exchangerates/rates/"

    startDate = endDate - timedelta(days=days)

    paramsUrl = "/{}/{}/{}".format(currencyCode, startDate, endDate)
    return requests.get(url + tableCode + paramsUrl)


def getUsdAndEurOverHalfOfYear(endDate=date.today()):
    return getAverageExchangeRatesInDays("USD", 182, endDate), getAverageExchangeRatesInDays("EUR", 182, endDate)
