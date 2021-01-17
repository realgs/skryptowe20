from datetime import datetime
from flask import jsonify
from server.app_config import *
from server.db_models import *
from server.api_exceptions import *

dateFormat = '%Y-%m-%d'


@app.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')


@app.route('/rates/<code>/<dateStr>', methods=['GET'])
def rateInDate(code, dateStr):
    try:
        datetime.strptime(dateStr, dateFormat)
    except Exception:
        raise BadRequest()
    exchangeRate = Exchange.objects(code=code.upper(), dateStr=dateStr)
    if len(exchangeRate) == 0:
        raise NoDataFound('No data found with code: {} and date: {}'.format(code.upper(), dateStr))
    return jsonify(exchangeRate)


@app.route('/rates/<code>/<startDateStr>/<endDateStr>', methods=['GET'])
@cache.memoize(600)
def ratesBetweenDates(code, startDateStr, endDateStr):
    try:
        startDate = datetime.strptime(startDateStr, dateFormat)
        endDate = datetime.strptime(endDateStr, dateFormat)
    except Exception:
        raise BadRequest()
    if startDate > endDate:
        raise BadRequest()
    exchangeRates = Exchange.objects(code=code.upper()).filter((Q(date__gte=startDate) & Q(date__lte=endDate))) \
        .order_by('date')
    if len(exchangeRates) == 0:
        raise NoDataFound(
            'No data found with code: {} and date range: <{}, {}>'.format(code.upper(), startDateStr, endDateStr))
    return jsonify(exchangeRates)


@app.route('/sales/<dateStr>', methods=['GET'])
def saleInDate(dateStr):
    try:
        datetime.strptime(dateStr, dateFormat)
    except Exception:
        raise BadRequest()
    sale = SalesResult.objects(dateStr=dateStr)
    if len(sale) == 0:
        raise NoDataFound('No data found with date: {}'.format(dateStr))
    return jsonify(sale)


@app.route('/sales/<startDateStr>/<endDateStr>', methods=['GET'])
@cache.memoize(600)
def salesBetweenDates(startDateStr, endDateStr):
    try:
        startDate = datetime.strptime(startDateStr, dateFormat)
        endDate = datetime.strptime(endDateStr, dateFormat)
    except Exception:
        raise BadRequest()
    if startDate > endDate:
        raise BadRequest()
    sales = SalesResult.objects().filter((Q(date__gte=startDate) & Q(date__lte=endDate))).order_by('date')
    if len(sales) == 0:
        raise NoDataFound(
            'No data found in date range: <{}, {}>'.format(startDateStr, endDateStr))
    return jsonify(sales)


@app.errorhandler(ApiException)
def handle_invalid_usage(error):
    return error.to_dict(), error.status_code


if __name__ == '__main__':
    app.run()
