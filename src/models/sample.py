from typing import Optional, List, Set

from pydantic import BaseModel, HttpUrl, Field

from models.common import IdBaseModel, LoggingBaseModel, QueryParameters, Terms, Contributor


class SampleUpdate(BaseModel):
    _schema: HttpUrl = Field(...)
    sample_code: str = Field(..., description='Sample code')
    collection_id: str = Field(..., description='Sample collection Id')
    parent_sample_code: Optional[str] = Field(None, description='Parent sample code')
    description: str = Field(..., description='Description of the sample')
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