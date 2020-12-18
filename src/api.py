from database.database import Database
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache


DB_NAME = "../Source/bazunia.db"

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

cache = Cache(config={'CACHE_TYPE': 'simple'})
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
    return jsonify(status=404, info="Data not found"), 404
  else:
    rates = [{'rate':x[0], 'date':x[1], 'interpolated':x[2] == 1 if True else False} for x in rates]
    return jsonify(rates=rates)


@app.route('/api/rates/<date>')
@cache.cached(timeout=50)
def return_rate(date):
  db = Database(DB_NAME)
  res = db.get_avg_usd_rates(date)
  if res == []:
    return jsonify(status=404, info="Data not found"), 404
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
    return jsonify(status=404, info="Data not found"), 404
  else:
    rates = [{'rate': x[0], 'date': x[1], 'interpolated': x[2] == 1 if True else False} for x in res]
    return jsonify(rates=rates)


@app.route('/api/sales/<start_date>/<end_date>')
@cache.cached(timeout=50)
def return_sales(start_date, end_date):
  db = Database(DB_NAME)
  res = db.get_sales_usd_pln(start_date, end_date)
  if res == []:
    return jsonify(status=404, info="Data not found"), 404
  else:
    sales = [{'date': x[0], 'usd': x[1], 'pln': x[2]} for x in res]
    return jsonify(sales=sales)


@app.route('/api/sales/<date>')
@cache.cached(timeout=50)
def return_sale(date):
  db = Database(DB_NAME)
  res = db.get_sales_usd_pln(date, date)

  if res == []:
    return jsonify(status=404, info="Data not found"), 404
  else:
    [(date, usd, pln)] = res
    return jsonify(date=date, usd=usd, pln=pln)


@app.errorhandler(429)
def handle_too_many_req(e):
  return jsonify(status=429, info="Too many requests!"), 429


@app.errorhandler(404)
def handle_bad_req(e):
  return jsonify(status=400, info="Bad request!"), 400


if __name__ == '__main__':

  app.run('0.0.0.0', port=8080, debug=True)
