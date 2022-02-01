from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

from models.common import IdBaseModel, LoggingBaseModel, QueryParameters, Contributor, Unit, State, Terms


class ProjectUpdate(BaseModel):
    project_code: str = Field(..., description='Project code (file number, acronym...)')
    unit: Unit = Field(...)
    category: str = Field(..., 
        description="Category identifier (a-z, 0-9, -, _)",
        min_length=1,
        max_length=20,
        regex='^[a-z0-9-_]*$') 
    template: Optional[str] = Field(None, 
        description="Template identifier (a-z, 0-9, -, _)",
        min_length=1,
        max_length=20,
        regex='^[a-z0-9-_]*$')
    subject: Optional[str] = Field(None, description='Subject of the project (e.g. project name or object title)')
    contributors: Optional[List[Contributor]] = Field(None, unique=True)
    state: State = Field(...)
    terms: Optional[Terms] = Field(None)
    pid: str = Field(...)
    path: str = Field(...)


class _ProjectShort(ProjectUpdate, IdBaseModel):
    pass


class Project(LoggingBaseModel, _ProjectShort):
    class Config:
        title = "Generic project"


class ProjectList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[_ProjectShort] = Field([])