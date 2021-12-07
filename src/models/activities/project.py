from typing import Set, Optional
from pydantic import Field

from .activity import Activity


class Project(Activity):

    class Config:
        title = "Project"