from enum import Enum
from typing import Set, Optional

from pydantic import BaseModel, Field
from .measurement import Measurement


class DRMSParameters(BaseModel):
    instrument: Optional[str]
    software: Optional[Set[str]]
    drill_type: Optional[str]
    radius: Optional[float]
    rotation_speed: Optional[int]
    penetration_rate: Optional[int]

    class Config:
        title = "Measurement parameters"


class DRMSResults(BaseModel):
    comments: Optional[str] = Field(None, title='Comments', description='Comments with regards to generated research data')

    class Config:
        title = "Measurement results"


class DRMS(Measurement):
    document_type: str = Field("Drilling resistance measurement system", title='Document type', const=True) #OVERRIDE FROM DOCUMENT
    measurement_parameters: Optional[DRMSParameters] = Field(None)
    measurement_results: Optional[DRMSResults] = Field(None)