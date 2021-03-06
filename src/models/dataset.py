from typing import Optional, List, Set

from pydantic import BaseModel, HttpUrl, Field

from models.common import IdBaseModel, LoggingBaseModel, QueryParameters, Terms, Contributor, Unit


class File(BaseModel):
    path: str = Field(..., title='Path', description='Path to a file or a directory')
    type: Optional[str] = Field(None, title="File type")


class Project(BaseModel):
    project_id: Optional[str] = Field(None, title='Project Id')
    project_code: Optional[str] = Field(None, description='Project code (file number, acronym...)')
    unit: Optional[Unit] = Field(None) 
    # Note:
    # These properties should actually not be optional, since the project-property in a Dataset is
    # itself optional. However, due to a bug in VJSF (https://github.com/koumoul-dev/vuetify-jsonschema-form/issues/230)
    # this was done as a temporary workaround


class Sample(BaseModel):
    sample_id: Optional[str] = Field(None, title='Sample Id')
    sample_code: Optional[str] = Field(None, description='Sample code')


class DatasetUpdate(BaseModel):
    _schema: HttpUrl = Field(...)
    dataset_code: str = Field(..., description='Dataset code')
    project: Optional[Project] = Field(None)
    object_id: Optional[int] = Field(None, description="Object number to which this dataset belongs")
    samples: Optional[List[Sample]] = Field(None)
    contributors: Optional[Set[Contributor]] = Field(None)
    terms: Optional[Terms] = Field(None)
    persistent_identifier: Optional[str] = Field(None, description='Persistent identifier for the dataset')
    files: Optional[List[File]] = Field(None)


class _DatasetShort(DatasetUpdate, IdBaseModel):
    pass


class Dataset(LoggingBaseModel, _DatasetShort):
    class Config:
        title = "Generic dataset"


class DatasetList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[_DatasetShort] = Field([])