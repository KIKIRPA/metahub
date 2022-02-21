from typing import Optional, List

from pydantic import BaseModel, HttpUrl, Field

from models.common import IdBaseModel, LoggingBaseModel, QueryParameters, Contributor, Unit, State, Terms


class ProjectUpdate(BaseModel):
    _schema: HttpUrl = Field(...) 
    project_code: str = Field(..., description='Project code (file number, acronym...)')
    unit: Unit = Field(...)
    subject: Optional[str] = Field(None, description='Subject of the project (e.g. project name or object title)')
    contributors: Optional[List[Contributor]] = Field(None, unique=True)
    state: State = Field(...)
    terms: Terms = Field(None)
    persistent_identifier: Optional[str] = Field(None, description='Persistent identifier for the project')
    path: Optional[str] = Field(None, description='Relative file path where the project data is stored')


class _ProjectShort(ProjectUpdate, IdBaseModel):
    pass


class Project(LoggingBaseModel, _ProjectShort):
    class Config:
        title = "Generic project"


class ProjectList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[_ProjectShort] = Field([])