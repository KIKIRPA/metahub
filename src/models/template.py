from enum import Enum
from typing import Type, Optional, List, Dict, Any
from datetime import datetime

from pydantic import BaseModel, Field

from models.app_base_model import AppBaseModel, Pagination

class Category(str, Enum):
    ACTIVITY = 'Activity'
    COLLECTION = 'Collection'
    SAMPLE = 'Sample'
    DOCUMENT = 'Document'


class Template(AppBaseModel): 
    category: Category = Field(..., 
        description="Category for which the template will be used in the application") 
    schema_id: str = Field(..., 
        description="Short identifier for the schema (a-z, 0-9, -, _)",
        min_length=1,
        max_length=20,
        regex='^[a-z0-9-_]*$') 
    template_id: str = Field("_default", 
        description="Short identifier for the template (a-z, 0-9, -, _)",
        min_length=1,
        max_length=20,
        regex='^[a-z0-9-_]*$')
    short_name: str = Field(...,
        description="Name for the schema or template",
        min_length=1,
        max_length=20)
    long_name: str = Field(..., 
        description="Name for the schema or template",
        min_length=1,
        max_length=100)
    selectable: bool = Field(False, description="Allow users to select this template")
    json_schema: dict = Field(..., description="JSON schema overlay")


class TemplateUpdate(BaseModel): # unique index on (category, schema_id and template_id)
    category: Category = Field(..., 
        description="Category for which the template will be used in the application") 
    schema_id: str = Field(..., 
        description="Short identifier for the schema (a-z, 0-9, -, _)",
        min_length=1,
        max_length=20,
        regex='^[a-z0-9-_]*$') 
    template_id: str = Field("_default", 
        description="Short identifier for the template (a-z, 0-9, -, _)",
        min_length=1,
        max_length=20,
        regex='^[a-z0-9-_]*$')
    short_name: str = Field(...,
        description="Name for the schema or template",
        min_length=1,
        max_length=20)
    long_name: str = Field(..., 
        description="Name for the schema or template",
        min_length=1,
        max_length=100)
    selectable: bool = Field(False, description="Allow users to select this template")
    json_schema: dict = Field(..., description="JSON schema overlay")



class TemplateList(BaseModel):
    pagination: Pagination = Field(...)
    data: List[Template] = Field([])