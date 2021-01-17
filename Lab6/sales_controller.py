from flask import Blueprint, request
from datetime import datetime
from database.commands import get_sales_for_date, get_sales_in_range
import json
from nbp_requests import MIN_ALLOWED_DATE, MAX_ALLOWED_DATE
from crossdomain_decorator import crossdomain

sales_controller = Blueprint("sales_controller", __name__)

@sales_controller.route('/api/sales/', methods=['GET'])
@crossdomain(origin='*')
def sales_for_day():
    request_params = request.args

    try:
        request_date = datetime.strptime(request_params.get("date"), "%Y-%m-%d").date()

        if request_date < MIN_ALLOWED_DATE or request_date > MAX_ALLOWED_DATE:
            return ("Date is out of database dates range", 204)

        query_result = get_sales_for_date(request_date)
        raw_response = list(map(lambda x: {"USD": x[0], "PLN": x[1]}, query_result))

        return json.dumps(raw_response, indent=4, default=str)
    except ValueError:
        return ("Bad request format", 400)

@sales_controller.route('/api/sales/range/', methods=['GET'])
@crossdomain(origin='*')
def sales_in_range():
    request_params = request.args

    try:
        from_date = datetime.strptime(request_params.get("from"), "%Y-%m-%d").date()
        to_date = datetime.strptime(request_params.get("to"), "%Y-%m-%d").date()

        if from_date < MIN_ALLOWED_DATE or to_date > MAX_ALLOWED_DATE:
            return ("Period is out of database dates range", 204)

        query_result = get_sales_in_range(from_date, to_date)
        raw_response = list(map(lambda x: {"date": x[0], "USD": x[1], "PLN": x[2]}, query_result))

        return json.dumps(raw_response, indent=4, default=str)
    except ValueError:
        return ("Bad request format", 400)