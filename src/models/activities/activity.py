from enum import Enum
from typing import Optional, List, Set
from pydantic import BaseModel, Field
from bson import ObjectId


class ActivityType(str, Enum):
    INTERVENTION_FILE = 'Intervention file'
    PROJECT = 'Project'


class Unit(str, Enum):
    PAINTING_LAB = 'Painting Lab'
    DENDRO_LAB = 'Dendrochrology Lab'

class Role(str, Enum):
    COORDINATOR = 'Coordinator'
    CO_COORDINATOR = 'Co-coordinator'
    COLLABORATOR = 'Collaborator'


class State(str, Enum):
    OPEN = 'Open'
    ARCHIVED = 'Archived'


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
    roles: Set[Role] = Field(Role.COLLABORATOR, title="Roles")


class Activity(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", title="Document Id")
    activity_type: ActivityType = Field(...)
    activity_id: str = Field(...)
    unit: Unit = Field(...)
    subject: Optional[str] = Field(None, description='Subject of the activity (e.g. project name or object title)')
    related_objects: Optional[Set[int]]
    contributors: Optional[List[Contributor]] = Field(None, unique=True)
    state: State = Field(State.OPEN)

    class Config:
        json_encoders = {ObjectId: str}
        title = "Activity"