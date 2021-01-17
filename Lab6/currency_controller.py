from flask import Blueprint, request
from datetime import datetime
from database.commands import get_currencies_in_range
import json
from nbp_requests import MIN_ALLOWED_DATE, MAX_ALLOWED_DATE
from crossdomain_decorator import crossdomain

currency_controller = Blueprint("currency_controller", __name__)

@currency_controller.route('/api/exchangerates/', methods=['GET'])
@crossdomain(origin='*')
def exchange_rates_in_range():
    request_params = request.args

    try:
        from_date = datetime.strptime(request_params.get("from"), "%Y-%m-%d").date()
        to_date = datetime.strptime(request_params.get("to"), "%Y-%m-%d").date()

        if from_date < MIN_ALLOWED_DATE or to_date > MAX_ALLOWED_DATE:
            return ("Period is out of database dates range", 204)

        query_result = get_currencies_in_range(from_date, to_date)
        raw_response = list(map(lambda x: {"date": x[1], "currency": x[2], "interpolated": x[3]}, query_result))

        return json.dumps(raw_response, indent=4, default=str)
    except ValueError:
        return ("Bad request format", 400)
