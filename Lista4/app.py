from flask import Flask, Response, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from db_connection import get_rates_from_to
import datetime
import decimal
import json

app = Flask(__name__)
# Used to limit number of requests per user // task 4
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5/minute"],
)

first_rate_measure_db = datetime.datetime.strptime('2015-12-21', '%Y-%m-%d')


# Used to serialize data returned by endpoints
# https://stackoverflow.com/a/22238613
def json_serializer(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError ("Type %s not serializable" % type(obj))


# Task 1 and 2 endpoint
@app.route('/rates/from/<date_from>/to/<date_to>', methods=['GET'])
def get_rates(date_from='', date_to=''):
    try:
        date_from_parsed = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        date_to_parsed = datetime.datetime.strptime(date_to, '%Y-%m-%d')
    except ValueError:
        return Response(request.remote_addr)
        return Response('Invalid date format', status=400)
    if date_from_parsed > date_to_parsed:
        return Response('date_from cannot be greater than date_to', status=400)
    if date_from_parsed < first_rate_measure_db or date_to_parsed > datetime.datetime.today() - datetime.timedelta(days=1):
        first_rate_measure_db_str = datetime.datetime.strftime(first_rate_measure_db, '%Y-%m-%d')
        today_str = datetime.datetime.strftime(datetime.date.today() - datetime.timedelta(days=1), '%Y-%m-%d')
        return Response('Date interval must be between ' + first_rate_measure_db_str + ' and ' + today_str, status=400)
    result = get_rates_from_to(date_from, date_to)
    return Response(json.dumps(result, default=json_serializer), status=200)


if __name__ == '__main__':
    app.run(debug=True)
    # todo caching
    # todo updatowanie bazki 
    # todo readme 
    # todo screeny xd
