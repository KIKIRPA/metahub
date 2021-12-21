from enum import Enum
from typing import Type, Optional, List, Dict, Any
from datetime import datetime

from pydantic import BaseModel, Field

from models.app_base_model import AppBaseModel, Pagination

class Resource(str, Enum):
    ACTIVITY = 'activity'
    COLLECTION = 'collection'
    SAMPLE = 'sample'
    DOCUMENT = 'document'


class Template(AppBaseModel): # unique index on (resource, category and template)
    resource: Resource = Field(..., 
        description="Resource for which the template will be used in the application") 
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
        description="Name for the template",
        min_length=1,
        max_length=20)
    long_name: str = Field(..., 
        description="Name for the template",
        min_length=1,
        max_length=100)
    selectable: bool = Field(False, description="Allow users to select this template")
    json_schema: dict = Field(..., description="JSON schema overlay")


class TemplateUpdate(BaseModel):
    resource: Resource = Field(..., 
        description="Resource for which the template will be used in the application") 
    category: str = Field(..., 
        description="Category identifier for the template (a-z, 0-9, -, _)",
        min_length=1,
        max_length=20,
        regex='^[a-z0-9-_]*$') 
    template: str = Field("_default", 
        description="Template identifier (a-z, 0-9, -, _)",
        min_length=1,
        max_length=20,
        regex='^[a-z0-9-_]*$')
    short_name: str = Field(...,
        description="Name for the template",
        min_length=1,
        max_length=20)
    long_name: str = Field(..., 
        description="Name for the template",
        min_length=1,
        max_length=100)
    selectable: bool = Field(False, description="Allow users to select this template")
    json_schema: dict = Field(..., description="JSON schema overlay")



class TemplateList(BaseModel):
    pagination: Pagination = Field(...)
    data: List[Template] = Field([])