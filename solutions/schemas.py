import datetime
from pydantic import BaseModel, Field
from bson import ObjectId

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class ExchangeRate(BaseModel):
    id: PyObjectId = Field(alias='_id')
    date: datetime.date
    pln_to_usd: float
    interpolated: bool
        
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class TransactionSummary(BaseModel):
    id: PyObjectId = Field(alias='_id')
    date: datetime.date
    pln: float
    usd: float
        
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
