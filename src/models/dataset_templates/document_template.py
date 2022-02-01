from pydantic import BaseModel, Field
from typing import Set
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


class DatasetTemplate(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", title="Dataset Id")
    alias: str = Field(..., description='Short and unique name for the template')
    title: str = Field(..., description='Descriptive name for the template')
    schemas: Set[str] = Field(..., description='Base schemas on which this template can be applied')
    template: dict = Field(..., description='JSON')

    class Config:
        json_encoders = {ObjectId: str}


class DatasetTemplateReduced(BaseModel):
    alias: str
    title: str
    schemas: Set[str]