from typing import Optional, List

from pydantic import BaseModel, HttpUrl, Field

from models.common import IdBaseModel, LoggingBaseModel, QueryParameters, Contributor, Unit, State, Terms


class ProjectUpdate(BaseModel):
    _schema: HttpUrl = Field(..., alias="$schema") 
    project_code: str = Field(..., description='Project code (file number, acronym...)')
    unit: Unit = Field(...)
    subject: Optional[str] = Field(None, description='Subject of the project (e.g. project name or object title)')
    contributors: Optional[List[Contributor]] = Field(None, unique=True)
    state: State = Field(...)
    terms: Optional[Terms] = Field(None)
    pid: str = Field(None)
    path: str = Field(None)


class _ProjectShort(ProjectUpdate, IdBaseModel):
    pass


class Project(LoggingBaseModel, _ProjectShort):
    class Config:
        title = "Generic project"


class ProjectList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[_ProjectShort] = Field([])