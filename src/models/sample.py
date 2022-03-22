from typing import Optional, List, Set

from pydantic import BaseModel, HttpUrl, Field

from models.common import IdBaseModel, LoggingBaseModel, QueryParameters, Terms, Contributor


class Collection(BaseModel):
    collection_id: str = Field(None, title='Sample collection Id')
    collection_name: str = Field(..., description='Unique sample collection name')


class ParentSample(BaseModel):
    sample_id: str = Field(None, title='Parent sample Id')
    sample_code: str = Field(..., description='Parent sample code')


class SampleUpdate(BaseModel):
    _schema: HttpUrl = Field(...)
    sample_code: str = Field(..., description='Sample code')
    collection: Collection = Field(...)
    parent_sample: Optional[ParentSample] = Field(None)
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