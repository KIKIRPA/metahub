from typing import Optional, List, Set
from enum import Enum
from datetime import datetime, date

from pydantic import BaseModel, Field


class Unit(str, Enum):          # may need to change to Literal to make it possible to add roles in the UI
    PAINTING_LAB = 'Painting Lab'
    DENDRO_LAB = 'Dendrochrology Lab'


class Role(str, Enum):          # may need to change to Literal to make it possible to add roles in the UI
    MAIN_COORDINATOR = 'Main coordinator'
    UNIT_COORDINATOR = 'Unit coordinator'
    COLLABORATOR = 'Collaborator'
    ANALYST = 'Analyst'
    AUTHOR = 'Author'
    OPERATOR = 'Operator'


class State(str, Enum):         # may need to change to Literal to make it possible to add roles in the UI
    OPEN = 'Open'
    REQUESTED = 'Closure requested'
    CLOSED = 'Closed'
    ARCHIVED = 'Published and archived'


class IdBaseModel(BaseModel):
    id: str = Field(...)


class LoggingBaseModel(BaseModel):
    created_timestamp: Optional[datetime] = Field(None)
    created_by_user: Optional[str] = Field(None)
    modified_timestamp: Optional[datetime] = Field(None)
    modified_by_user: Optional[str] = Field(None)


class QueryParameters(BaseModel):
    find: Optional[dict] = Field({})
    sort_by: Optional[List[str]] = Field([])
    sort_desc: Optional[List[bool]] = Field([])
    skip: Optional[int] = Field(0)
    limit: Optional[int] = Field(10)
    total: int = Field(...)




class Terms(BaseModel):
    license: str            # may need to change to Literal
    access: str             # may need to change to Literal
    embargo: date


class Contributor(BaseModel):
    contributor_id: str = Field(..., title='Contributor Id')
    roles: Set[Role] = Field(None, title="Roles")