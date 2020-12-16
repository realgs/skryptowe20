import flask
from datetime import datetime, timedelta
from flask import request, jsonify
from edit_database import connect_to_database
from edit_database import execute_inserting_values
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# const values used to validate task 1 - could be also select min/max
MIN_START_DATE = '2015-01-02'
MAX_END_DATE = '2017-12-28'

# setting connection and flask
conn = connect_to_database()
app = flask.Flask(__name__)
app.config["DEBUG"] = True
app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,  # get users IP address.
    default_limits=["300000 per month"],  # default limit to 300K request per month
)


# available dates in total value of transactions - task 3
def fetch_available_dates_tansactions():
    cur = conn.cursor()
    cur.execute('''SELECT transactionsdate from transactionssums''')
    dates = cur.fetchall()
    cur.close()
    return list(map(lambda x: datetime.strftime(x[0], '%Y-%m-%d'), dates))


AVAILABLE_DATES_TRANSACTIONS = fetch_available_dates_tansactions()
BASE_LIMIT = "10 per minute"


# helper func to transform list of data into json with titles
def format_item_json(item):
    return {'daterate': datetime.strftime(item[0], '%Y-%m-%d'), 'rate': item[1], 'interpolated': item[2]}


# task 1
@app.route('/exchangerates', methods=['GET'])
@limiter.limit(BASE_LIMIT)
def get_exchangerates_from_period():
    start_date = None
    end_date = None
    if 'startDate' in request.args:
        start_date = request.args['startDate']
    if 'endDate' in request.args:
        end_date = request.args['endDate']
    if start_date is None or start_date == '':
        start_date = MIN_START_DATE
    if end_date is None or end_date == '':
        end_date = MAX_END_DATE
    if start_date < MIN_START_DATE or end_date > MAX_END_DATE:
        return "<h1>404</h1><p>Data could not be fetched due to wrong start/end date.</p>", 404

    sql_select_data = f''' SELECT * FROM exchangerates WHERE ratedate BETWEEN '{start_date}' AND '{end_date}' '''
    cur = conn.cursor()
    cur.execute(sql_select_data)
    data = cur.fetchall()
    conn.commit()
    cur.close()
    return jsonify(list(map(format_item_json, data)))


# task 2
# modified method from lab4 to insert interpolation property - code below
# deleted data and added column in postgres with command 'ALTER TABLE exchangerates; ADD COLUMN interpolated boolean;'
def fill_gaps_in_dates(dates_and_rates):
    filled_dates = []
    rates = []
    interpolations = []
    for i in range(len(dates_and_rates) - 1):
        next_day = datetime.strptime(dates_and_rates[i + 1]['effectiveDate'], '%Y-%m-%d')
        curr_day = datetime.strptime(dates_and_rates[i]['effectiveDate'], '%Y-%m-%d')
        if next_day - curr_day > timedelta(days=1):
            temp_date = curr_day
            while temp_date < next_day:
                filled_dates.append(temp_date.strftime('%Y-%m-%d'))
                rates.append(dates_and_rates[i]['mid'])
                if temp_date == curr_day:
                    interpolations.append(False)
                else:
                    interpolations.append(True)
                temp_date = temp_date + timedelta(days=1)
        else:
            filled_dates.append(dates_and_rates[i]['effectiveDate'])
            rates.append(dates_and_rates[i]['mid'])
            interpolations.append(False)
    return filled_dates, rates, interpolations


def setInterpolation():
    execute_inserting_values(conn)  # method from lab4


# task 3 - new table creation
def create_table_transactions_by_day():
    sql_create_table = '''
        CREATE TABLE IF NOT EXISTS TransactionsSums (
        TransactionsDate date,
        UsdAmount double precision,
        PlnAmount double precision)
        '''
    cur = conn.cursor()
    cur.execute(sql_create_table)
    cur.close()
    conn.commit()


# task 3 - adding data (total value of transactions grouped by day)
def populate_transactions_table():
    select_query = '''select bought "date", round as "sum usd", ROUND(rate*round) "sum pln" from (select bought, 
    ROUND(SUM(averageprice *  totalvolume)) from pythonlab group by bought order by bought) as TransactionData join exchangerates on 
    TransactionData.bought = exchangerates.ratedate '''
    cur = conn.cursor()
    cur.execute(select_query)
    data_to_insert = cur.fetchall()
    values_to_insert = ''
    for i in range(len(data_to_insert)):
        values_to_insert += f"('{data_to_insert[i][0]}', {data_to_insert[i][1]}, {data_to_insert[i][2]} ), "
    values_to_insert = values_to_insert[0:len(values_to_insert) - 2]
    print(values_to_insert)
    cur.execute("INSERT INTO TransactionsSums VALUES %s" % values_to_insert)
    cur.close()
    conn.commit()


# task 3 - get transactions sum in a single day
@app.route('/transactions', methods=['GET'])
@limiter.limit(BASE_LIMIT)
def get_sum_from_day():
    if 'day' in request.args:
        day = request.args['day']
    else:
        return "<p>You should give the date in query params.</p>"
    print(day)
    print(day in AVAILABLE_DATES_TRANSACTIONS)
    if day not in AVAILABLE_DATES_TRANSACTIONS:
        return f'''<p>This date is not in a database</p>
        <p>Available dates: {AVAILABLE_DATES_TRANSACTIONS} '''
    select_query = f"SELECT * from TransactionsSums WHERE transactionsdate = '{day}' "
    cur = conn.cursor()
    cur.execute(select_query)
    transaction_data = cur.fetchone()
    cur.close()
    return jsonify({'date': datetime.strftime(transaction_data[0], '%Y-%m-%d'), 'usdAmount': transaction_data[1],
                    'plnAmount': transaction_data[2]})


@app.route('/', methods=['GET'])
@limiter.limit(BASE_LIMIT)
def home():
    return '''<h1>API for getting rate exchanges</h1>
<p>Tell me what you need in the URL :)</p>
<p>Heads up - available dates for exchangerates are 2015-01-02 to 2018-12-28 </p>
<p>And for total transaction values are since  every 7 days </p> '''


@app.errorhandler(404)
def page_not_found():
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == '__main__':
    # setInterpolation()
    # create_table_transactions_by_day()
    # populate_transactions_table()
    app.run()
