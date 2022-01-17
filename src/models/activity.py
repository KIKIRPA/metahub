from enum import Enum
from typing import Optional, List
from datetime import date

from pydantic import BaseModel, Field

from models.common import IdBaseModel, LoggingBaseModel, QueryParameters


class Unit(str, Enum):          # may need to change to Literal to make it possible to add roles in the UI
    PAINTING_LAB = 'Painting Lab'
    DENDRO_LAB = 'Dendrochrology Lab'


class Role(str, Enum):          # may need to change to Literal to make it possible to add roles in the UI
    MAIN_COORDINATOR = 'Main coordinator'
    UNIT_COORDINATOR = 'Unit coordinator'
    COLLABORATOR = 'Collaborator'


class State(str, Enum):         # may need to change to Literal to make it possible to add roles in the UI
    OPEN = 'Open'
    REQUESTED = 'Closure requested'
    CLOSED = 'Closed'
    ARCHIVED = 'Published and archived'


class Contributor(BaseModel):
    contributor_id: str = Field(..., title='Contributor Id')
    role: Role = Field(...)


class Terms(BaseModel):
    license: str            # may need to change to Literal to make it possible to add roles in the UI
    access: str             # may need to change to Literal to make it possible to add roles in the UI
    embargo: date


class ActivityUpdate(BaseModel):
    code: str = Field(..., description='Intervention number, project acronym...')
    unit: Unit = Field(...)
    subject: Optional[str] = Field(None, description='Subject of the activity (e.g. project name or object title)')
    contributors: Optional[List[Contributor]] = Field(None, unique=True)
    state: State = Field(...)
    terms: Optional[Terms] = Field(None)


class _ActivityShort(ActivityUpdate, IdBaseModel):
    pass


class Activity(LoggingBaseModel, _ActivityShort):
    class Config:
        title = "Generic activity"


class ActivityList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[_ActivityShort] = Field([])