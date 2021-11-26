from enum import Enum
from typing import Set, Optional

from pydantic import BaseModel, Field
from .measurement import Measurement


class Grating(BaseModel):
    grating_type: Optional[str]
    grating_density: Optional[int]

    class Config:
        title = "Grating"


class LaserPower(BaseModel):
    laser_power_at_sample: Optional[float]
    neutral_density_filtering: Optional[float]

    class Config:
        title = "Laser power"


class RejectionFilters(BaseModel):
    filter_type:  Optional[str]
    cutoff_frequency: Optional[float]

    class Config:
        title = "Rejection filters"


class SpectralRange(BaseModel):
    spectral_range_low: Optional[float]
    spectral_range_high: Optional[float]

    class Config:
        title = "Spectral range"


class RamanParameters(BaseModel):
    instrument: Optional[str]
    software: Set[str]
    detector_type: Optional[str]
    instrument_class: Optional[str]
    accessory: Optional[str]
    excitation_source: Optional[float]
    laser_power: LaserPower
    spectral_range: SpectralRange
    filters: RejectionFilters
    grating: Grating
    resolution: Optional[float]
    laser_defocus: Optional[bool]
    data_collection: Optional[str]
    integration_time: Optional[float]
    accumulations: Optional[int]
    objective: Optional[str]
    spot_size: Optional[float]
    confocality: Optional[bool]
    polarization: Optional[str]
    data_processing: Set[str]

    class Config:
        title = "Measurement Parameters"


class RamanResults(BaseModel):
    identified_components: Set[str] = Field(None, title='Identified components')
    comments: Optional[str] = Field(None, title='Comments', description='Comments with regards to generated research data')

    class Config:
        title = "Measurement Results"


class Raman(Measurement):
    document_type: str = Field("Micro-Raman Spectrometry", title='Document type', const=True) #OVERRIDE FROM DOCUMENT
    measurement_parameters: Optional[RamanParameters] = Field(None)
    results: Optional[RamanResults] = Field(None)

