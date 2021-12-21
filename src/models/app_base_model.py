from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, Field


class AppBaseModel(BaseModel):
    id: str = Field(...)
    created_timestamp: Optional[datetime] = Field(None)
    created_by_user: Optional[str] = Field(None)
    modified_timestamp: Optional[datetime] = Field(None)
    modified_by_user: Optional[str] = Field(None)


class QueryParameters(BaseModel):
    find: Optional[dict] = Field({})
    sort_by: Optional[List[str]] = Field([])
    sort_desc: Optional[List[bool]] = Field([])
    skip: Optional[int] = Field(0)
    limit: Optional[int] = Field(10)
    total: int = Field(...)