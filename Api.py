from datetime import datetime
from flask import jsonify
from appConfig import *
from dbModels import *
from ApiExceptions import *

dateFormat = '%Y-%m-%d'


@app.route('/', methods=['GET'])
def index():
    return """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"> <title>Currency exchange and sales api</title> 
    <h1>Currency exchange and sales api</h1> <h3>Get exchange rates</h3> <h4>Posible routes:</h4> 
    <p>/rates/{code}/{date} - returns the exchange rate for the {Code} currency on {date} </p> 
    <p>/rates/{code}/{startDate}/{endDate} - returns the exchange rates for the {Code} currency between {startDate} 
    and {endDate}</p> 
    <h3>Get sales results</h3> <h4>Posible routes:</h4> 
    <p>/sales/{date} - returns the sales result on {date}</p>
    <p>/sales/{startDate}/{endDate} - returns the sales results between {startDate} and {endDate}</p>
    <br><br>
    <p>{code} - three letter currency code</p>
    <p>{date},{startDate},{endDate} - date in format: "yyyy-mm-dd"</p>
    """


@app.route('/rates/<code>/<dateStr>', methods=['GET'])
def rateInDate(code, dateStr):
    try:
        datetime.strptime(dateStr, dateFormat)
    except Exception:
        raise BadRequest()
    exchangeRate = Exchange.objects(code=code.upper(), dateStr=dateStr)
    if len(exchangeRate) == 0:
        raise NoDataFound('No data found with code: {} and date: {}'.format(code.upper(), dateStr))
    return jsonify(exchangeRate[0])


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
    exchangeRates = Exchange.objects(code=code.upper()).filter((Q(date__gte=startDate) & Q(date__lte=endDate)))
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
    return jsonify(sale[0])


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
    sales = SalesResult.objects().filter((Q(date__gte=startDate) & Q(date__lte=endDate)))
    if len(sales) == 0:
        raise NoDataFound(
            'No data found in date range: <{}, {}>'.format(startDateStr, endDateStr))
    return jsonify(sales)


@app.errorhandler(ApiException)
def handle_invalid_usage(error):
    return error.to_dict(), error.status_code


if __name__ == '__main__':
    app.run()
