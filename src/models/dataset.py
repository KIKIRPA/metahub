from enum import Enum
from typing import Optional, List, Set

from pydantic import BaseModel, Field

from models.common import IdBaseModel, LoggingBaseModel, QueryParameters


class Role(str, Enum):
    ANALYST = 'Analyst'
    AUTHOR = 'Author'
    OPERATOR = 'Operator'


class Contributor(BaseModel):
    contributor_id: str = Field(..., title='Contributor Id')
    roles: Set[Role] = Field(None, title="Roles")


class File(BaseModel):
    path: str = Field(..., title='Path', description='Path to a file or a directory')
    format: Optional[str] = Field(None, title="File format")


class DatasetUpdate(BaseModel):
    dataset_type: str = Field(...)
    dossier_id: str = Field(..., title='Dossier/project Id')
    object_id: Optional[int] = Field(None, description="Object number to which this dataset belongs")
    contributors: Optional[Set[Contributor]] = Field(...)
    files: Optional[Set[File]] = Field(...)


class _DatasetShort(DatasetUpdate, IdBaseModel):
    pass


class Dataset(LoggingBaseModel, _DatasetShort):
    class Config:
        title = "Generic dataset"


class DatasetList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[_DatasetShort] = Field([])