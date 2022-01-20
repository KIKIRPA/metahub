from datetime import date
from typing import Set, Optional

from pydantic import BaseModel, Field
from .dataset import Dataset


class MeasurementId(BaseModel):
    measurement_technique: Optional[str] = Field(None, title='Analytical technique code')
    measurement_date: Optional[date] = Field(None, title='Measurement date')
    measurement_index: Optional[str] = Field(None, title='Measurement index')

    class Config:
        title = "Measurement Identifier"

class Sample(BaseModel):
    sample_id: str


class Measurement(Dataset):
    measurement_id: MeasurementId = Field(...)
    samples: Optional[Set[Sample]] = Field(..., title='Samples')

    class Config:
        title = "Measurement"