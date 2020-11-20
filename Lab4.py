import datetime
import requests
import json

DAYS_IN_YEAR = 365
DAYS_LIMIT = 92


def daysRange(xDays):
    if not isinstance(xDays, int):
        raise TypeError('Wrong type of parameter (daysRange)')
    if xDays <= 0:
        raise ValueError('Negativ days (daysRange)')

    today = datetime.datetime.date(datetime.datetime.now())
    previousDate = today - datetime.timedelta(days=xDays)
    dateRanges = []

    while (today - previousDate).days > DAYS_LIMIT:
        prev = previousDate
        next = previousDate + datetime.timedelta(days=DAYS_LIMIT)
        dateRanges.append((prev, next))
        previousDate = next + datetime.timedelta(days=1)

    dateRanges.append((previousDate, today))

    return dateRanges


def apiUrl(table, currency, fromDate, toDate):
    if not table.isalpha() or not isinstance(currency, str) or not isinstance(fromDate, datetime.date) or not isinstance(toDate, datetime.date):
        raise TypeError('Wrong instance of one of the parameters (apiUrl)')

    return f'http://api.nbp.pl/api/exchangerates/rates/{table}/{currency}/{fromDate}/{toDate}'

#Zad1
def midCurrFromXDays(currency, xDays):
    dateRanges = daysRange(xDays)
    results = []

    for dateR in dateRanges:
        aTableUrl = apiUrl('a', currency, dateR[0], dateR[1])
        ra = requests.get(aTableUrl)


        if ra.status_code != 200:
            raise ra.exceptions.RequestException(f"Request for {aTableUrl} returned code {ra.status_code}: {ra.text}")
        elif ra.status_code == 404:
            return None
        else:
            results.append(json.loads(ra.text))

    for i in range(1, len(results)):
        results[0]['rates'] = results[0]['rates'] + results[i]['rates']

    if len(results):
        return results[0]
    else:
        return results


if __name__ == '__main__':
    print(daysRange(180))
    #Zad2
    print(json.dumps(midCurrFromXDays('eur', DAYS_IN_YEAR // 2), indent=3))
    print(json.dumps(midCurrFromXDays('usd', DAYS_IN_YEAR // 2), indent=3))
