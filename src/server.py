from flask import Flask, jsonify, abort
from nbp_api import DATE_FORMAT
import database as db
from database import datetime, NoSuchTableError

app = Flask(__name__)

time = 365 * 20
currencies = ['eur', 'usd']

@app.route('/currency/<currency>/today')
def get_rete_of_currency_from_today(currency):
    try:
        today = datetime.today().strftime(DATE_FORMAT)
        res = db.get_between(currency, today, today)
        if(len(res) > 0):
            return jsonify(res)
        else:
            abort(400, 'Could not find currency rates in given period')
    except TypeError:
        abort(400, 'Wrong parameter types')
    except ValueError:
        abort(400, 'Time was not valid')
    except NoSuchTableError:
        abort(400, 'Such table does not extist')

@app.route('/currency/<currency>/<day>')
def get_rete_of_currency_from_given_day(currency, day):
    try:
        res = db.get_between(currency, day, day)
        if(len(res) > 0):
            return jsonify(res)
        else:
            abort(400, 'Could not find currency rate in given day')
    except TypeError:
        abort(400, 'Wrong parameter types')
    except ValueError:
        abort(400, 'Time was not valid')
    except NoSuchTableError:
        abort(400, 'Such table does not extist')

@app.route('/currency/<currency>/<begin>/<end>')
def get_rete_of_currency_between(currency, begin, end):
    try:
        res = db.get_between(currency, begin, end)
        if(len(res) > 0):
            return jsonify(res)
        else:
            abort(400, 'Could not find currency rates in given period')
    except TypeError:
        abort(400, 'Wrong parameter types')
    except ValueError:
        abort(400, 'Time was not valid')
    except NoSuchTableError:
        abort(400, 'Such table does not extist')


@app.route('/currency/<currency>/last/<int:days>')
def get_rete_of_currency_last_days(currency, days):
    try:
        res = db.get_last(currency, days)
        if(len(res) > 0):
            return jsonify(res)
        else:
            abort(400, 'Could not find currency rates in given period')
    except TypeError:
        abort(400, 'Wrong parameter types')
    except ValueError:
        abort(400, 'Integer must be positive')
    except NoSuchTableError:
        abort(400, 'Such table does not extist')

if __name__ == "__main__":
    for currency in currencies:
        db.create_and_fill_currency_table(currency, time)

    app.run()
