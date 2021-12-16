from enum import Enum
from typing import Optional
from datetime import datetime

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


class Category(str, Enum):
    ACTIVITY = 'Activity'
    COLLECTION = 'Collection'
    SAMPLE = 'Sample'
    DOCUMENT = 'Document'


class Template(BaseModel): # unique index on (category, schema_id and template_id)
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    category: Category = Field(..., 
        description="Category for which the template will be used in the application") 
    schema_id: str = Field(..., 
        description="Short identifier for the schema (a-z, 0-9, -, _)",
        min_length=1,
        max_length=15,
        regex='^[a-z0-9-_]*$') 
    template_id: str = Field("_default", 
        description="Short identifier for the template (a-z, 0-9, -, _)",
        min_length=1,
        max_length=15,
        regex='^[a-z0-9-_]*$')
    short_name: str = Field(...,
        description="Name for the schema or template",
        min_length=1,
        max_length=15)
    long_name: str = Field(..., 
        description="Name for the schema or template",
        min_length=1,
        max_length=100)
    selectable: bool = Field(False, description="Allow users to select this template")
    json_schema: dict = Field(..., description="JSON schema overlay")
    created_timestamp: Optional[datetime] = Field(None)
    created_by_user: Optional[str] = Field(None)
    modified_timestamp: Optional[datetime] = Field(None)
    modified_by_user: Optional[str] = Field(None)

    class Config:
        json_encoders = {ObjectId: str}

