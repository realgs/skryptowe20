from database.database import Database
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from conf import conf, API_ERROR_NOT_FOUND, API_ERROR_BAD_REQ, API_ERROR_TOO_MANY_REQS


DB_NAME = conf['db']['db_name']

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=conf['limits']
)

cache = Cache(config=conf['cache'])
cache.init_app(app)


@app.route('/api/home/<name>')
@cache.cached(timeout=50)
def home(name):
  return jsonify(hello= "Hello",
              world=name)


@app.route('/api/rates')
@cache.cached(timeout=50)
def return_all_rates():
  db = Database(DB_NAME)
  rates = db.get_avg_usd_rates()
  if rates == []:
    return jsonify(error=API_ERROR_NOT_FOUND), API_ERROR_NOT_FOUND['status']
  else:
    rates = [{'rate':x[0], 'date':x[1], 'interpolated':x[2] == 1 if True else False} for x in rates]
    return jsonify(rates=rates)


@app.route('/api/rates/<date>')
@cache.cached(timeout=50)
def return_rate(date):
  db = Database(DB_NAME)
  res = db.get_avg_usd_rates(date)
  if res == []:
    return jsonify(error=API_ERROR_NOT_FOUND), API_ERROR_NOT_FOUND['status']
  else:
    [(rate, date, interpolated)] = res
    return jsonify(rate=rate,
                  date=date,
                  interpolated= interpolated == 1 if True else False
    )


@app.route('/api/rates/<start>/<end>')
@cache.cached(timeout=50)
def return_rates(start, end):
  db = Database(DB_NAME)
  res = db.get_avg_usd_rates_in_interval(start, end)
  if res == []:
    return jsonify(error=API_ERROR_NOT_FOUND), API_ERROR_NOT_FOUND['status']
  else:
    rates = [{'rate': x[0], 'date': x[1], 'interpolated': x[2] == 1 if True else False} for x in res]
    return jsonify(rates=rates)


@app.route('/api/sales/<start_date>/<end_date>')
@cache.cached(timeout=50)
def return_sales(start_date, end_date):
  db = Database(DB_NAME)
  res = db.get_sales_usd_pln(start_date, end_date)
  if res == []:
    return jsonify(error=API_ERROR_NOT_FOUND), API_ERROR_NOT_FOUND['status']
  else:
    sales = [{'date': x[0], 'usd': x[1], 'pln': x[2]} for x in res]
    return jsonify(sales=sales)


@app.route('/api/sales/<date>')
@cache.cached(timeout=50)
def return_sale(date):
  db = Database(DB_NAME)
  res = db.get_sales_usd_pln(date, date)

  if res == []:
    return jsonify(error=API_ERROR_NOT_FOUND), API_ERROR_NOT_FOUND['status']
  else:
    [(date, usd, pln)] = res
    return jsonify(date=date, usd=usd, pln=pln)


@app.errorhandler(429)
def handle_too_many_req(e):
  return jsonify(error=API_ERROR_TOO_MANY_REQS), API_ERROR_TOO_MANY_REQS['status']


@app.errorhandler(404)
def handle_bad_req(e):
  return jsonify(error=API_ERROR_BAD_REQ), API_ERROR_BAD_REQ['status']


if __name__ == '__main__':
  app.run(conf['api']['host'], port=conf['api']['port'], debug=conf['api']['debug'])
