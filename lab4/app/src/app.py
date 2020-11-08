from datetime import datetime, timedelta
from decimal import Decimal
from flask import Flask, render_template
from dbManager import DataAccessObject
from nbpRatesReceiver import get_currency_rates

CHARTS_TEMPLATE = 'charts.html'
DB_CONFIG = 'dbConfig.json'
DOLLAR_CODE = 'USD'
EURO_CODE = 'EUR'


def mix_dollar_euro_rates(dollar_result, euro_result):
    dollar_response, dollar_status = dollar_result
    euro_response, euro_status = euro_result
    if dollar_status == 200 and euro_status == 200:
        dollar_rates = dollar_response['rates']
        euro_rates = euro_response['rates']
        rates = []
        for i in range(len(dollar_rates)):
            rates.append({
                "date": dollar_rates[i]['date'],
                "dollarRate": dollar_rates[i]['rate'],
                "euroRate": euro_rates[i]['rate']
            })
        return {"rates": rates}, 200
    else:
        return dollar_result if dollar_status != 200 else euro_result


def create_daily_orders(daily_orders_total_usd_amount, daily_rate, previous_date):
    return {
        "date": str(previous_date),
        "totalAmountUsd": float(daily_orders_total_usd_amount),
        "totalAmountPln": round(float(daily_orders_total_usd_amount * daily_rate[previous_date]), 2)
    }


def calculate_daily_orders(usd_rates, orders):
    daily_orders = []
    if len(orders) > 0:
        daily_rate = {}
        for usd_rates in usd_rates:
            daily_rate[usd_rates['date']] = usd_rates['plnRate']

        previous_date = orders[0]['date']
        daily_orders_total_usd_amount = Decimal('0.00')
        for order in orders:
            order_date = order['date']
            if order_date == previous_date:
                daily_orders_total_usd_amount += order['totalAmount']
            else:
                daily_orders.append(create_daily_orders(daily_orders_total_usd_amount, daily_rate, previous_date))
                previous_date = order_date
                daily_orders_total_usd_amount = order['totalAmount']
        daily_orders.append(create_daily_orders(daily_orders_total_usd_amount, daily_rate, previous_date))
    return daily_orders


app = Flask(__name__)
dao = None


@app.route('/')
def receive_main_chart():
    return render_template(CHARTS_TEMPLATE)


@app.route('/api/rates')
def receive_dollar_euro_rates():
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=182)
    dollar_result = get_currency_rates(DOLLAR_CODE, start_date, end_date)
    euro_result = get_currency_rates(EURO_CODE, start_date, end_date)
    return mix_dollar_euro_rates(dollar_result, euro_result)


@app.route('/api/daily_orders')
def receive_rates():
    usd_rates = dao.read_usd_pln_rates()
    orders = dao.read_orders()
    return {"dailyOrders": calculate_daily_orders(usd_rates, orders)}


if __name__ == '__main__':
    dao = DataAccessObject(DB_CONFIG)
    app.run(debug=False, host='0.0.0.0', port=8080)
