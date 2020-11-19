import requests
from datetime import date, datetime, timedelta

enDolar = "USD"
enEuro = "EUR"
currDate = date.today()

def averageRateDays(value, number):
    
    tempDate = currDate
    back = {}
    quantity = 0
    
    while (quantity < number):
        
        getApi = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/A/{value}/{tempDate.strftime("%Y-%m-%d")}/')

        if getApi.status_code != 200:
            pass
        else:

            back[ tempDate.strftime("%Y-%m-%d") ] = getApi.json()['rates'][0]['mid']
            quantity += 1

        tempDate = tempDate - timedelta( days = 1 )

    return back

def halfYearDolarEuro():

    fromDate = (currDate - timedelta(days=190)).strftime("%Y-%m-%d")
    toDate = currDate.strftime("%Y-%m-%d")

    getApiDolars = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/A/{enDolar}/{fromDate}/{toDate}/')
    getApiEuro = requests.get(f'http://api.nbp.pl/api/exchangerates/rates/A/{enEuro}/{fromDate}/{toDate}/')

    arrDol = {}
    arrEur = {}

    if getApiEuro.status_code != 200:
        pass
    else:
        for x in getApiEuro.json()['rates']:
            arrEur[str(x['effectiveDate'])] = x['mid']

    if getApiDolars.status_code != 200:
        pass
    else:
        for x in getApiDolars.json()['rates']:
            arrDol[str(x['effectiveDate'])] = x['mid']

    return arrDol, arrEur
    