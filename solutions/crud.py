from sqlalchemy.orm import Session
from fastapi import File, UploadFile,  HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from bson.objectid import ObjectId
from fastapi import HTTPException
import schemas
import pymongo
import datetime

def check_dates(start_date, end_date=None):
    if start_date > datetime.date.today():
        raise HTTPException(status_code=416, detail="Wrong date (there is no data from the future")

    if end_date is not None:
        if end_date > datetime.date.today():
            raise HTTPException(status_code=416, detail="Wrong date (there is no data from the future")

        if end_date < start_date:
            raise HTTPException(status_code=416, detail='End date should be later than start date')

def _get_exchange_rates_list(collection):
    exchange_rates = []
    for exchange_rate in collection:
        exchange_rates.append(schemas.ExchangeRate(**exchange_rate))
    return exchange_rates

def get_exchange_rates(collection: pymongo.collection.Collection):
    return {'exchange_rates': _get_exchange_rates_list(collection.find())}

def get_exchange_rate(collection: pymongo.collection.Collection, date: datetime.date):
    check_dates(date)
    date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0, 0)
    exchange_rate = collection.find_one({"date": date})
    if exchange_rate:
        return schemas.ExchangeRate(**exchange_rate)
    else:
        raise HTTPException(status_code=416, detail="Data for this date isn't available")

def get_exchange_rates_in_range(collection: pymongo.collection.Collection, start_date: datetime.date, end_date: datetime.date):
    check_dates(start_date, end_date)
    start_date = datetime.datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0, 0)
    end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, 0, 0, 0, 0)
    exchange_rates = collection.find({"date": 
    {
        "$gte": start_date,
        "$lte": end_date}
    })    
    if exchange_rates:
        return {'exchange_rates': _get_exchange_rates_list(exchange_rates)}
    else:
        raise HTTPException(status_code=416, detail="Data for this range isn't available")

def get_transaction_sum_in_day(collection: pymongo.collection.Collection, date: datetime.date):
    date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0, 0)
    exchange_rate = collection.find_one({"date": date})
