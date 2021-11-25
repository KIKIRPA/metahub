from enum import Enum
from typing import Set, Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class Role(str, Enum):
    analyst = 'Analyst'
    author = 'Author'
    operator = 'Operator'


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


class Document(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", title="Document Id")
    document_type: str = Field(..., title='Document type')
    dossier_id: str = Field(..., title='Dossier/project Id')
    contributors: Set[Contributor] = Field(...)
    files: Set[File] = Field(...)

    class Config:
        json_encoders = {ObjectId: str}
