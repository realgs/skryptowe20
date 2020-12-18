from database.database import Database
from flask import Flask, jsonify, request
import sqlite3


DB_NAME = "../Source/bazunia.db"

app = Flask(__name__)


@app.route('/api/home/<name>')
def home(name):
  return jsonify(hello= "Hello",
              world=name)


@app.route('/api/rates')
def return_rates():
  db = Database(DB_NAME)
  rates = db.get_avg_usd_rates()
  rates = [{'rate':x[0], 'date':x[1], 'interpolated':x[2] == 1 if True else False} for x in rates]
  return jsonify(rates=rates)


@app.route('/api/rates/<date>')
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


@app.route('/api/sales/<start_date>/<end_date>')
def return_sales(start_date, end_date):
  db = Database(DB_NAME)
  res = db.get_sales_usd_pln(start_date, end_date)
  if res == []:
    return jsonify(status=404, info="Data not found"), 404
  else:
    sales = [{'date': x[0], 'usd': x[1], 'pln': x[2]} for x in res]
    return jsonify(sales=sales)


@app.route('/api/sales/<date>')
def return_sale(date):
  db = Database(DB_NAME)
  res = db.get_sales_usd_pln(date, date)

  if res == []:
    return jsonify(status=404, info="Data not found"), 404
  else:
    [(date, usd, pln)] = res
    return jsonify(date=date, usd=usd, pln=pln)


if __name__ == '__main__':

  app.run('0.0.0.0', port=8080, debug=True)
