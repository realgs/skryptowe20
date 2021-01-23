import datetime
import aioredis
from functools import lru_cache

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi.encoders import jsonable_encoder

import crud
import schemas
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from pymongo import MongoClient
from slowapi import Limiter
from slowapi.util import get_remote_address

OBJECTS_LIST_LIMIT = '5 per minute'
SIMPLE_OBJECT_LIMIT = '50 per minute'
limiter = Limiter(key_func=get_remote_address, default_limits=["300 per day"])
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = MongoClient()
db = client['sample_supplies']


@lru_cache(256)
def get_collection(coll_name='PLN_exchange_rates'):
    return db[coll_name]


@app.get('/api/exchangerates')
@limiter.limit(OBJECTS_LIST_LIMIT)
@cache(expire=60)
async def read_exchange_rates(request: Request):
    collection = get_collection()
    return jsonable_encoder(crud.get_exchange_rates(collection=collection))


@app.get('/api/exchangerates/{date}', response_model=schemas.ExchangeRate)
@limiter.limit(SIMPLE_OBJECT_LIMIT)
@cache(expire=60)
async def read_exchange_rate(request: Request, date: datetime.date):
    collection = get_collection()
    return jsonable_encoder(crud.get_exchange_rate(collection=collection, date=date))


@limiter.limit(OBJECTS_LIST_LIMIT)
@app.get('/api/exchangerates/{start_date}/{end_date}')
@cache(expire=60)
async def read_exchange_rates_in_range(request: Request, start_date: datetime.date, end_date: datetime.date):
    collection = get_collection()
    return jsonable_encoder(crud.get_exchange_rates_in_range(collection=collection, start_date=start_date, end_date=end_date))


@limiter.limit(SIMPLE_OBJECT_LIMIT)
@app.get('/api/transactions/{date}')
@cache(expire=60)
async def read_transaction_sum_in_day(request: Request, date: datetime.date):
    collection = get_collection('transaction_summary')
    return jsonable_encoder(crud.get_transaction_sum_in_day(collection=collection, date=date))

@limiter.limit(OBJECTS_LIST_LIMIT)
@app.get('/api/transactions/{start_date}/{end_date}')
@cache(expire=60)
async def read_transaction_sum_in_range(request: Request, start_date: datetime.date, end_date: datetime.date):
    collection = get_collection('transaction_summary')
    return jsonable_encoder(crud.get_transaction_sum_in_range(collection=collection, start_date=start_date, end_date=end_date))



@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool("redis://localhost", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
