from datetime import date
from typing import Set, Optional

from pydantic import BaseModel, Field
from .document import Document


class Sample(BaseModel):
    sample_id: str


class Measurement(Document):
    analytical_technique: str = Field(..., title='Analytical technique')
    measurement_date: Optional[date] = Field(None, title='Measurement date')
    measurement_index: Optional[str] = Field(None, title='Measurement index')
    samples: Set[Sample] = Field(..., title='Samples')

