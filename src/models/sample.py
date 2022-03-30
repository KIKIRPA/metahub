from typing import Optional, List, Set

from pydantic import BaseModel, HttpUrl, Field

from models.common import IdBaseModel, LoggingBaseModel, QueryParameters, Terms, Contributor, Unit


class Collection(BaseModel):
    collection_id: str = Field(None, title='Sample collection Id')
    collection_name: str = Field(..., description='Unique sample collection name')


class ParentSample(BaseModel):
    parent_sample_id: Optional[str] = Field(None, title='Parent sample Id')
    parent_sample_code: Optional[str] = Field(None, description='Parent sample code')


class Project(BaseModel):
    project_id: Optional[str] = Field(None, title='Project Id')
    project_code: Optional[str] = Field(None, description='Project code (file number, acronym...)')
    unit: Optional[Unit] = Field(None) 
    # Note:
    # These properties should actually not be optional, since the project-property in a Dataset is
    # itself optional. However, due to a bug in VJSF (https://github.com/koumoul-dev/vuetify-jsonschema-form/issues/230)
    # this was done as a temporary workaround


class SampleUpdate(BaseModel):
    _schema: HttpUrl = Field(...)
    sample_code: str = Field(..., description='Sample code')
    collection: Collection = Field(...)
    parent_sample: Optional[ParentSample] = Field(None)
    projects: Optional[Set[Project]] = Field(None)
    description: Optional[str] = Field(None, description='Description of the sample')
    contributors: Optional[Set[Contributor]] = Field(...)
    terms: Optional[Terms] = Field(None)
    persistent_identifier: Optional[str] = Field(None, description='Persistent identifier for the sample')


class _SampleShort(SampleUpdate, IdBaseModel):
    pass


class Sample(LoggingBaseModel, _SampleShort):
    class Config:
        title = "Generic sample"


class SampleList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[_SampleShort] = Field([])