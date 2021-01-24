from datetime import datetime, timedelta
import requests


def get_currency_from_period(currency, date_from, date_to):
    table_type = 'a'
    resp = requests.get(
        f'http://api.nbp.pl/api/exchangerates/rates/{table_type}/{currency}/{date_from}/{date_to}/?format=json')
    if resp.status_code == 200:
        data = resp.json()['rates']
        # print(data[0]['effectiveDate'][-2:])
        for record in data:
            record.pop('no', None)
            record['interpolated'] = False
        if data[0]['effectiveDate'] != date_from:
            if int(data[0]['effectiveDate'][-2:]) - int(date_from[-2:]) == 1:
                print(1)
                date_sunday = {'effectiveDate': datetime.strftime(
                    datetime.strptime(data[0]['effectiveDate'], "%Y-%m-%d") - timedelta(days=1), "%Y-%m-%d"),
                               'mid': data[0]['mid'], 'interpolated': True}
                data.insert(0, date_sunday)
            elif int(data[0]['effectiveDate'][-2:]) - int(date_from[-2:]) == 2:
                print(2)
                date_saturday = {'effectiveDate': datetime.strftime(
                    datetime.strptime(data[0]['effectiveDate'], "%Y-%m-%d") - timedelta(days=2), "%Y-%m-%d"),
                                 'mid': data[0]['mid'], 'interpolated': True}
                date_sunday = {'effectiveDate': datetime.strftime(
                    datetime.strptime(data[0]['effectiveDate'], "%Y-%m-%d") - timedelta(days=1), "%Y-%m-%d"),
                                 'mid': data[0]['mid'], 'interpolated': True}
                data.insert(0, date_sunday)
                data.insert(0, date_saturday)
        return data
    print("Error with code {}".format(resp.status_code))


def get_currency_last_x_days(currency, days):
    date_to = datetime.today().strftime('%Y-%m-%d')
    date_from = (datetime.today() - timedelta(days)).strftime('%Y-%m-%d')
    output = get_currency_from_period(currency, date_from, date_to)
    return output
