from typing import Optional, List, Set

from pydantic import BaseModel, HttpUrl, Field

from models.common import IdBaseModel, LoggingBaseModel, QueryParameters, Terms, Contributor


class CollectionUpdate(BaseModel):
    _schema: HttpUrl = Field(...)
    collection_name: str = Field(..., description='Unique sample collection name')
    description: Optional[str] = Field(None, description='Description of the collection')
    storage_location: Optional[str] = Field(None, description='Physical location of the collection')
    contributors: Optional[Set[Contributor]] = Field(...)
    terms: Optional[Terms] = Field(None)
    persistent_identifier: Optional[str] = Field(None, description='Persistent identifier for the sample collection')


class _CollectionShort(CollectionUpdate, IdBaseModel):
    pass


class Collection(LoggingBaseModel, _CollectionShort):
    class Config:
        title = "Generic sample collection"


class CollectionList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[_CollectionShort] = Field([])


class CollectionCompact(IdBaseModel):
    collection_name: str = Field(...)