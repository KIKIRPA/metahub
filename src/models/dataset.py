from typing import Optional, List, Set

from pydantic import BaseModel, HttpUrl, Field

from models.common import IdBaseModel, LoggingBaseModel, QueryParameters, Terms, Contributor


class File(BaseModel):
    path: str = Field(..., title='Path', description='Path to a file or a directory')
    format: Optional[str] = Field(None, title="File format")


class DatasetUpdate(BaseModel):
    _schema: HttpUrl = Field(...)
    dataset_code: str = Field(..., description='Dataset code')
    project_id: str = Field(..., title='Project Id')
    object_id: Optional[int] = Field(None, description="Object number to which this dataset belongs")
    contributors: Optional[Set[Contributor]] = Field(...)
    terms: Optional[Terms] = Field(None)
    persistent_identifier: Optional[str] = Field(None, description='Persistent identifier for the dataset')
    files: Optional[Set[File]] = Field(...)


class _DatasetShort(DatasetUpdate, IdBaseModel):
    pass


class Dataset(LoggingBaseModel, _DatasetShort):
    class Config:
        title = "Generic dataset"


class DatasetList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[_DatasetShort] = Field([])