from datetime import date
from typing import List

from pydantic import BaseModel
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class MeasurementId(BaseModel):
    technique: str
    date: date
    index: int


class Sample(BaseModel):
    id: str
    collection: str


class Measurement(BaseModel):
    id: MeasurementId
    sample: List[Sample]
    characteristic: str
    material: List[str]
