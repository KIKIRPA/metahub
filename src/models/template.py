from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

from models.common import IdBaseModel, LoggingBaseModel, QueryParameters

class Resource(str, Enum):
    ACTIVITY = 'activity'
    COLLECTION = 'collection'
    SAMPLE = 'sample'
    DOCUMENT = 'document'


class _TemplateMeta(BaseModel): # unique index on (resource, category and template)
    resource: Resource = Field(...) 
    category: str = Field(..., 
        description="Category identifier (a-z, 0-9, -, _)",
        min_length=1,
        max_length=20,
        regex='^[a-z0-9-_]*$') 
    template: str = Field("_default", 
        description="Template identifier (a-z, 0-9, -, _)",
        min_length=1,
        max_length=20,
        regex='^[a-z0-9-_]*$')
    short_name: str = Field(...,
        description="Short descriptive name or acronym for the template",
        min_length=1,
        max_length=20)
    title: str = Field(..., 
        description="Title of the template (and of the resulting schema)",
        min_length=1,
        max_length=100)
    selectable: bool = Field(False, description="Allow users to select this template")


class _TemplateJson(BaseModel): 
    independent_schema: bool = Field(False, description="An independent schema does not inherit from a base schema")
    json_schema: dict = Field(..., description="JSON schema overlay")


class _TemplateShort(_TemplateMeta, IdBaseModel):
    pass


class TemplateUpdate(_TemplateJson, _TemplateMeta):
    pass


class Template(LoggingBaseModel, TemplateUpdate, IdBaseModel):
    pass


class TemplateList(BaseModel):
    query_parameters: QueryParameters = Field(...)
    data: List[_TemplateShort] = Field([])