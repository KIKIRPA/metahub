from enum import Enum
from typing import Set, Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class Role(str, Enum):
    ANALYST = 'Analyst'
    AUTHOR = 'Author'
    OPERATOR = 'Operator'


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


class Contributor(BaseModel):
    contributor_id: str = Field(..., title='Contributor Id')
    roles: Set[Role] = Field(None, title="Roles")


class File(BaseModel):
    path: str = Field(..., title='Path', description='Path to a file or a directory')
    format: Optional[str] = Field(None, title="File format")


class Dataset(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", title="Dataset Id")
    dataset_type: str = Field(...)
    dossier_id: str = Field(..., title='Dossier/project Id')
    object_id: Optional[int] = Field(None, description="Object number to which this dataset belongs")
    contributors: Optional[Set[Contributor]] = Field(...)
    files: Optional[Set[File]] = Field(...)

    class Config:
        json_encoders = {ObjectId: str}
        title = "Dataset"
