from typing import Set, Optional
from pydantic import Field

from .activity import Activity


class InterventionFile(Activity):
    #intervention_file_id: str = Field(...)
    #related_objects: Optional[Set[int]]

    class Config:
        title = "Intervention file"