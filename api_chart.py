import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt


API_URL = "http://api.nbp.pl/api"
DATE_FORMAT = "%Y-%m-%d"
DAYS_LIMIT = 365


def average_exchange_rates(currency, last_x_days):
    cur_dates = []
    cur_prices = []

    if last_x_days <= 0:
        raise ValueError("Number of days cannot be lower than 1")

    while last_x_days > 0:
        date_to = datetime.datetime.now()
        date_from = date_to - datetime.timedelta(days=last_x_days-1)

        if last_x_days >= DAYS_LIMIT:
            date_to = date_from + datetime.timedelta(days=DAYS_LIMIT-1)

        date_to = date_to.strftime(DATE_FORMAT)
        date_from = date_from.strftime(DATE_FORMAT)

        request_url = f"{API_URL}/exchangerates/rates/A/{currency}/{date_from}/{date_to}/"
        response = requests.get(request_url)

        if response.status_code != 200:
            raise Exception('GET /tasks/ {}'.format(response.status_code))

        cur_dates += [(i['effectiveDate']) for i in response.json()["rates"]]
        cur_prices += [i["mid"] for i in response.json()["rates"]]

        last_x_days -= DAYS_LIMIT

    return cur_dates, cur_prices


def fill_missing_data(date_from, date_to, dates, rates):
    date_from = datetime.datetime.strptime(date_from, DATE_FORMAT)
    date_to = datetime.datetime.strptime(date_to, DATE_FORMAT)
    all_dates = pd.date_range(date_from, date_to, freq='d').format()
    all_rates = []

    for i in range(len(all_dates)):
        if all_dates[i] in dates:
            all_rates.append(rates[dates.index(all_dates[i])])
        else:
            if len(all_rates) != 0:
                all_rates.append(all_rates[len(all_rates)-1])
            else:
                all_rates.append(round(sum(rates)/len(rates), 4))
    return all_dates, all_rates


def average_exchange_rates_between(currency, date_from, date_to):
    local_date_to = datetime.datetime.strptime(date_to, DATE_FORMAT)
    date_from = datetime.datetime.strptime(date_from, DATE_FORMAT)
    dates_delta = (local_date_to - date_from).days
    cur_dates = []
    cur_prices = []

    if dates_delta < 0:
        raise ValueError("Given range is not correct")

    while dates_delta >= 0:
        if dates_delta >= DAYS_LIMIT:
            local_date_to = date_from + datetime.timedelta(days=DAYS_LIMIT-1)

        local_date_to = local_date_to.strftime(DATE_FORMAT)
        date_from = date_from.strftime(DATE_FORMAT)

        request_url = f"{API_URL}/exchangerates/rates/A/{currency}/{date_from}/{local_date_to}/"
        response = requests.get(request_url)

        if response.status_code != 200:
            raise Exception('GET /tasks/ {}'.format(response.status_code))

        cur_dates += [(i['effectiveDate']) for i in response.json()["rates"]]
        cur_prices += [i["mid"] for i in response.json()["rates"]]
        local_date_to = datetime.datetime.strptime(local_date_to, DATE_FORMAT)
        date_from = local_date_to
        local_date_to = datetime.datetime.strptime(date_to, DATE_FORMAT)

        dates_delta -= DAYS_LIMIT

    return cur_dates, cur_prices


def plot_data(cur1_dates, cur1_prices, cur2_dates, cur2_prices):
    df1 = pd.DataFrame({'dates': cur1_dates, 'prices': cur1_prices})
    df1['dates'] = [pd.to_datetime(i) for i in df1['dates']]

    df2 = pd.DataFrame({'dates': cur2_dates, 'prices': cur2_prices})
    df2['dates'] = [pd.to_datetime(i) for i in df2['dates']]

    plt.plot(df1['dates'], df1['prices'], label="USD")
    plt.plot(df2['dates'], df2['prices'], label="EURO")

    plt.gcf().autofmt_xdate()
    plt.xlabel('Date [YYYY-MM-DD]')
    plt.ylabel('Exchange rate [PLN]')
    plt.legend(['USD rates', 'EURO rates'])
    plt.title('Average exchange rate of USD and EURO to PLN')
    plt.show()


if __name__ == '__main__':
    day_range = 366/2

    usd_dates, usd_rates = average_exchange_rates("USD", day_range)
    euro_dates, euro_rates = average_exchange_rates("EUR", day_range)

    plot_data(usd_dates, usd_rates, euro_dates, euro_rates)
