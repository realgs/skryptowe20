import flask
from flask import jsonify
import constans
from data_verifiers import date_format_ok, db_contains_year
from cache import rates

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/rates/<date>', methods=['GET'])
def get_rate_for_date(date):
    if not date_format_ok(date):
        return jsonify(error='Invalid date format'), constans.BAD_REQUEST

    if not db_contains_year(date):
        return jsonify(error='There is no data for given year'), constans.NOT_FOUND

    return jsonify(date=date, interpolated=rates[date]['interpolated'], rate=rates[date]['rate']), constans.OK


app.run()
