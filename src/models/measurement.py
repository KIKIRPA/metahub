from datetime import date
from typing import List

from pydantic import BaseModel
from .document import Document


class MeasurementId(BaseModel):
    technique: str
    date: date
    index: int


class Sample(BaseModel):
    id: str
    collection: str


class Measurement(Document):
    id: MeasurementId
    sample: List[Sample]
    characteristic: str
    material: List[str]

