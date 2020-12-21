#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI, UploadFile, Request, File, HTTPException, Depends
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import datetime
import crud, schemas
import json
import uvicorn
from pymongo import MongoClient

OBJECTS_LIST_LIMIT = '1 per minute'
SIMPLE_OBJECT_LIMIT = '10 per minute'
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

client = MongoClient()
db = client['sample_supplies']

def get_collection():
    client = MongoClient()
    db = client['sample_supplies']

    return db['PLN_exchange_rates']

collection = get_collection()

@app.get('/api/exchangerates')
@limiter.limit(OBJECTS_LIST_LIMIT)
async def read_exchange_rates(request: Request):
    return crud.get_exchange_rates(collection=collection)

@app.get('/api/exchangerates/{date}', response_model=schemas.ExchangeRate)
@limiter.limit(SIMPLE_OBJECT_LIMIT)
async def read_exchange_rate(request: Request, date: datetime.date):
    return crud.get_exchange_rate(collection=collection, date=date)

@limiter.limit(OBJECTS_LIST_LIMIT)
@app.get('/api/exchangerates/{start_date}/{end_date}')
async def read_exchange_rates_in_range(request: Request, start_date: datetime.date, end_date: datetime.date):
    return crud.get_exchange_rates_in_range(collection=collection, start_date=start_date, end_date=end_date)

@limiter.limit(SIMPLE_OBJECT_LIMIT)
@app.get('/api/transactions/{date}')
async def read_transaction_sum_in_day(request: Request, date: datetime.date):
    return crud.get_transaction_sum_in_day(collection=collection, date=date)

if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)
