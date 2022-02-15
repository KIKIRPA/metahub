from typing import Optional, Literal, List, Set
from enum import Enum
from datetime import datetime, date

from pydantic import BaseModel, Field


'''
For some Enums and Literals might be usefull to make them user-configurable at some point.
This won't work with Enums or Literals as far as I know.
Alternative solution: work with lists (or any other iterable) and use a custom validator:
https://stackoverflow.com/questions/65465555/how-to-use-values-from-list-as-pydantic-validator
'''

class Unit(str, Enum):
    PAINTING_LAB = 'Painting Lab'
    DENDRO_LAB = 'Dendrochronology Lab'


class Role(str, Enum):
    COORDINATOR = 'Coordinator'
    COLLABORATOR = 'Collaborator'
    ANALYST = 'Analyst'
    AUTHOR = 'Author'
    OPERATOR = 'Operator'
    ARCHIVIST = 'Archivist'


class State(str, Enum):
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
    access: Literal['Public', 
        'Restricted access',
        'Private'] = Field('Public', description='Access modalities')
    license: Literal[
        'Creative Commons Attribution 4.0 (CC-BY 4.0)', 
        'Creative Commons Public Domain (CC0)'] = Field('Creative Commons Attribution 4.0 (CC-BY 4.0)', description='The license that describes the terms')
    embargo: Optional[date] = Field(None, description='Date on which the imposed embargo expires')


class Contributor(BaseModel):
    contributor_id: str = Field(..., title='Contributor Id')
    roles: Set[Role] = Field(None, title="Roles")