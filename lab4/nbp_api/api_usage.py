import requests
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from jsonmerge import merge, Merger

max_days_for_one_query = 93


def currency_from_last_x_days(currency, x):
    jsons = []
    while x > max_days_for_one_query:
        response = requests.get("http://api.nbp.pl/api/exchangerates/rates/A/{}/{}/{}".
                                format(currency, datetime.date.today() - datetime.timedelta(days=x),
                                       datetime.date.today() - datetime.timedelta(days=x-92)))
        x -= 93
        jsons.append(response.json())
    response = requests.get("http://api.nbp.pl/api/exchangerates/rates/A/{}/{}/{}".
                            format(currency, datetime.date.today() - datetime.timedelta(days=x),
                                   datetime.date.today()))
    jsons.append(response.json())
    schema = {
        "properties": {
            "rates": {
                "mergeStrategy": "append"
            }
        }
    }
    merger = Merger(schema)
    answer = jsons[0]
    for i in range(1, jsons.__len__()):
        answer = merger.merge(answer, jsons[i])
    return answer


def create_usd_eur_price_graph(days):
    usd = currency_from_last_x_days("USD", days)
    eur = currency_from_last_x_days("EUR", days)
    dates = []
    values_eur = []
    values_usd = []
    for i in range(len(usd['rates'])):
        dates.append(usd['rates'][i]['effectiveDate'])
        values_eur.append(eur['rates'][i]['mid'])
        values_usd.append(usd['rates'][i]['mid'])
    fig, ax = plt.subplots()
    plt.plot(dates, values_eur, color='blue')
    plt.plot(dates, values_usd, color='green')
    eur_patch = mpatches.Patch(color='blue', label='Euro')
    usd_patch = mpatches.Patch(color='green', label='USD')
    plt.legend(handles=[eur_patch, usd_patch])
    plt.xlabel('Date')
    plt.ylabel('Price PLN')
    plt.title('Euro and USD prices in last {} days'.format(days))
    plt.xticks(dates[::int(days/20)])
    fig.autofmt_xdate()
    plt.show()


def main():
    create_usd_eur_price_graph(183)  # half a year
