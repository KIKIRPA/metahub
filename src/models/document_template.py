from pydantic import BaseModel, Field
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


class Document(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", title="Document Id")
    alias: str = Field(..., description='Short and unique name for the template')
    title: str = Field(..., description='Descriptive name for the template')
    schema: str = Field(..., description='Base schema on which this template must be applied')
    template: str = Field(..., description='JSON')

    class Config:
        json_encoders = {ObjectId: str}
