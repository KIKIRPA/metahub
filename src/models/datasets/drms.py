from enum import Enum
from typing import Set, Optional

from pydantic import BaseModel, Field
from .measurement import Measurement


class DRMSParameters(BaseModel):
    instrument: Optional[str] = Field(None, description="Name and specifications of the instrument used")
    software: Optional[Set[str]] = Field(None, description="Acquisition and data treatment software used")
    drill_type: Optional[str] = Field(None, description="Type of drill used")
    radius: Optional[float] = Field(None, description="Radius of the drilled hole in mm")
    rotation_speed: Optional[int] = Field(None, description="Constant rotation speed of the drilling motor in rpm")
    penetration_rate: Optional[int] = Field(None, description="Penetration rate in mm/min ")

    class Config:
        title = "Measurement parameters"


class DRMSResults(BaseModel):
    comments: Optional[str] = Field(None, title='Comments', description='Comments with regards to generated research data')

    class Config:
        title = "Measurement results"


class DRMS(Measurement):
    dataset_type: str = Field("drms", const=True) #OVERRIDE FROM DATASET
    measurement_parameters: Optional[DRMSParameters] = Field(None)
    measurement_results: Optional[DRMSResults] = Field(None)

    class Config:
        title = "Drilling resistance measurement"