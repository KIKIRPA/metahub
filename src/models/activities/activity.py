from enum import Enum
from typing import Set, Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class ActivityType(str, Enum):
    intervention_file = 'Intervention file'
    project = 'Project'


class Unit(str, Enum):
    painting_lab = 'Painting Lab'
    dendro_lab = 'Dendrochrology Lab'

class Role(str, Enum):
    analyst = 'Analyst'
    author = 'Author'
    operator = 'Operator'


class State(str, Enum):
    open = 'Open'
    archived = 'Archived'


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


class Activity(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", title="Document Id")
    activity_type: ActivityType = Field(...)
    unit: Unit = Field(...)
    contributors: Optional[Set[Contributor]] = Field(...)
    subject: Optional[str] = Field(None, description='Subject of the activity (e.g. project name or object title)')
    state: State = Field(State.open)

    class Config:
        json_encoders = {ObjectId: str}
        title = "Activity"
