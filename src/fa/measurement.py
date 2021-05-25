from datetime import date
from typing import List

from pydantic import BaseModel


class MeasurementId(BaseModel):
    technique: str
    date: date
    index: int


class Sample(BaseModel):
    id: str
    collection: str


class Measurement(BaseModel):
    id: MeasurementId
    sample: List[Sample]
    characteristic: str
    material: List[str]
