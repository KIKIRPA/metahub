from enum import Enum
from typing import Optional, List, Set
from pydantic import BaseModel, Field
from bson import ObjectId


class ProjectType(str, Enum):
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
    role: Role = Field(...)


class Project(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id", title="Document Id")
    project_type: ProjectType = Field(...)
    project_id: str = Field(...)
    unit: Unit = Field(...)
    subject: Optional[str] = Field(None, description='Subject of the project (e.g. project name or object title)')
    related_objects: Optional[List[int]]
    contributors: Optional[List[Contributor]] = Field(None, unique=True)
    state: State = Field(...)

    class Config:
        json_encoders = {ObjectId: str}
        title = "Project"