import requests

def _url(path):
    return 'http://api.nbp.pl/api' + path

def averageExchangeRate(currency, days):
    ratesArr = []
    req = requests.get(_url(f'/exchangerates/rates/a/{currency}/last/{days}'))
    if req.status_code != 200:
        print('SOMETHING WENT WRONG')
    else:
        for rate in req.json()['rates']:
            ratesArr.append(rate['mid'])
    return ratesArr, req
