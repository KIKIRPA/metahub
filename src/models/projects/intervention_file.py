from typing import Set, Optional
from pydantic import Field

from .project import Project


class InterventionFile(Project):
    #intervention_file_id: str = Field(...)
    #related_objects: Optional[Set[int]]

    class Config:
        title = "Intervention file"