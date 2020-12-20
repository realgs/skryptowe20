from datetime import datetime
from flask import jsonify
from dbConfig import *
from ApiExceptions import *

dateFormat = '%Y-%m-%d'


@app.route('/rates/<code>/<dateStr>', methods=['GET'])
def rateInDate(code, dateStr):
    exchangeRate = Exchange.objects(code=code.upper(), dateStr=dateStr)
    if len(exchangeRate) == 0:
        raise NoDataFound('No data found with code: {} and date: {}'.format(code.upper(), dateStr))
    return jsonify(exchangeRate[0])


@app.route('/rates/<code>/<startDateStr>/<endDateStr>', methods=['GET'])
def ratesBetweenDates(code, startDateStr, endDateStr):
    try:
        startDate = datetime.strptime(startDateStr, dateFormat)
        endDate = datetime.strptime(endDateStr, dateFormat)
    except Exception:
        raise BadRequest()

    exchangeRates = Exchange.objects(code=code.upper()).filter((Q(date__gte=startDate) & Q(date__lte=endDate)))
    if len(exchangeRates) == 0:
        raise NoDataFound(
            'No data found with code: {} and date range: <{}, {}>'.format(code.upper(), startDateStr, endDateStr))
    return jsonify(exchangeRates)


@app.route('/sales/<dateStr>', methods=['GET'])
def saleInDate(dateStr):
    sale = SalesResult.objects(dateStr=dateStr)
    if len(sale) == 0:
        raise NoDataFound('No data found with date: {}'.format(dateStr))
    return jsonify(sale[0])


@app.route('/sales/<startDateStr>/<endDateStr>', methods=['GET'])
def salesBetweenDates(startDateStr, endDateStr):
    try:
        startDate = datetime.strptime(startDateStr, dateFormat)
        endDate = datetime.strptime(endDateStr, dateFormat)
    except Exception:
        raise BadRequest()
    sales = SalesResult.objects().filter((Q(date__gte=startDate) & Q(date__lte=endDate)))
    if len(sales) == 0:
        raise NoDataFound(
            'No data found in date range: <{}, {}>'.format( startDateStr, endDateStr))
    return jsonify(sales)


@app.errorhandler(ApiException)
def handle_invalid_usage(error):
    return error.to_dict(), error.status_code


app.run()
