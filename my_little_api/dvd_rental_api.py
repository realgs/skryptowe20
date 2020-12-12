from datetime import datetime

import flask
import sqlalchemy
from flask import jsonify, request
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

import to_dictionary

app = flask.Flask(__name__)
app.config["DEBUG"] = True

DB_URI = "postgres://postgres:bazman@localhost:5432/dvdrental"
engine = sqlalchemy.create_engine(DB_URI)
conn = engine.connect()
Base = automap_base()
Base.prepare(conn, reflect=True)

# cache
exchange_rates_cache = {}
min_date = None
max_date = None


@app.route('/', methods=['GET'])
def home():
    return "<h1>DVD Rental Shop API</h1><p>This site is a prototype API for checking certaind DVD rental shop sales.</p>"


@app.route('/api/v1/resources/exchangerates', methods=['GET'])
def api_exchangerates():
    start_date = None
    end_date = None
    results = {}
    index = 1
    is_correct = True

    # Get Variables
    if 'startdate' in request.args:
        try:
            start_date = datetime.strptime(request.args['startdate'], '%d/%m/%y').date()
            if start_date < min_date:
                results['error_001'] = "DECLARED START DATE LOWER THAN MIN DATE. OMIT PARAMETER TO USE MIN DATE."
                is_correct = False
        except ValueError:
            results['error_003'] = "WRONG START DATE FORMAT. PLEASE USE DD/MM/YY FORMAT."
            is_correct = False

    if 'enddate' in request.args:
        try:
            end_date = datetime.strptime(request.args['enddate'], '%d/%m/%y').date()
            if end_date > max_date:
                results['error_002'] = "DECLARED END DATE HIGHER THAN MAX DATE. OMIT PARAMETER TO USE MAX DATE."
                is_correct = False
        except ValueError:
            results['error_004'] = "WRONG END DATE FORMAT. PLEASE USE DD/MM/YY FORMAT."
            is_correct = False

    # Process
    if is_correct:
        if start_date is not None:
            if end_date is not None:
                for i in range(exchange_rates_cache.__len__()):
                    test = exchange_rates_cache[i]
                    if start_date <= exchange_rates_cache[i]['date'] <= end_date:
                        results[index] = exchange_rates_cache[i]
                        index += 1
            else:
                for i in range(exchange_rates_cache.__len__()):
                    test = exchange_rates_cache[i]
                    if start_date <= exchange_rates_cache[i]['date']:
                        results[index] = exchange_rates_cache[i]
                        index += 1
        else:
            if end_date is not None:
                for i in range(exchange_rates_cache.__len__()):
                    test = exchange_rates_cache[i]
                    if exchange_rates_cache[i]['date'] <= end_date:
                        results[index] = exchange_rates_cache[i]
                        index += 1
            else:
                results = exchange_rates_cache

    # Return
    return jsonify(results)


def on_start():
    Session = sessionmaker(bind=conn)
    session = Session()
    global exchange_rates_cache
    exchange_rates_cache = to_dictionary.model_to_dict(session.query(Base.classes.exchange_rate).all())
    global min_date
    min_date = exchange_rates_cache[0]['date']
    global max_date
    max_date = exchange_rates_cache[exchange_rates_cache.__len__() - 1]['date']


def main():
    # prepare data
    on_start()
    # run app
    app.run()


main()
