from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from drms import DRMS
from raman import Raman


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
    raman: Optional[Raman]
    drms: Optional[DRMS]
