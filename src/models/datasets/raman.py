from enum import Enum
from typing import Set, Optional

from pydantic import BaseModel, Field
from .measurement import Measurement


class Grating(BaseModel):
    grating_type: Optional[str] = Field(None, description="Type of grating")
    grating_density: Optional[int] = Field(None, description="Line density of grating in dispersive Raman instrument in lines/mm")

    class Config:
        title = "Grating"


class LaserPower(BaseModel):
    laser_power_at_sample: Optional[float] = Field(None, description="Laser power at sample in mW")
    neutral_density_filtering: Optional[float] = Field(None, description="Laser power reduction by neutral density filters expressed in %")

    class Config:
        title = "Laser power"


class RejectionFilters(BaseModel):
    filter_type:  Optional[str] = Field(None, description="Optical filters used to prevent stray light from reaching spectrometer/detector")
    cutoff_frequency: Optional[float] = Field(None, description="Low frequency cut-off in 1/cm")

    class Config:
        title = "Rejection filters"


class SpectralRange(BaseModel):
    spectral_range_low: Optional[float] = Field(None, description="Lowest value of the spectral range expressed in Raman shift (1/cm)")
    spectral_range_high: Optional[float] = Field(None, description="Highest value of the spectral range expressed in Raman shift (1/cm)")

    class Config:
        title = "Spectral range"


class RamanParameters(BaseModel):
    instrument: Optional[str] = Field(None, description="Spectrometer manufacturer and model")
    software: Optional[Set[str]] = Field(None, description="Acquisition and data treatment software used")
    detector_type: Optional[str] = Field(None, description="Type of detector")
    instrument_class: Optional[str] = Field(None, description="Instrument Class (dispersive, Fourier transform)")
    accessory: Optional[str] = Field(None, description="Name and model of accessories")
    excitation_source_wavelength: Optional[float] = Field(None, description="Laser line wavelength in nanometers (nm)")
    laser_power: Optional[LaserPower] = Field(None)
    spectral_range: Optional[SpectralRange] = Field(None)
    filters: Optional[RejectionFilters] = Field(None)
    grating: Optional[Grating] = Field(None)
    resolution: Optional[float] = Field(None, description="Resolution of spectrum as measured in wavenumbers (1/cm)")
    data_collection: Optional[str] = Field(None, description="Raman acquisition mode, static or scanned")
    integration_time: Optional[float] = Field(None, description="Integration or dwell time in seconds")
    accumulations: Optional[int] = Field(None, description="Number of accumulations used (co-added) to produce spectrum")
    objective: Optional[str] = Field(None, description="Objective lens magnification, numerical aperture, working distance and series")
    spot_size: Optional[float] = Field(None, description="Laser spot diameter (nm) as determined by laser wavelength and microscope objective. Laser spot diameter = 1.22 (λ)/NA, where λ=wavelength, NA= numerical aperture.")
    confocality: Optional[bool] = Field(None, description="Use of confocal optical arrangement")
    laser_defocus: Optional[bool] = Field(None, description="Defocusing of laser")
    polarization: Optional[str] = Field(None, description="Y or N for polarization of excitation radiation with degrees and orientation followed by Y or N for polarization of scattered radiation with degrees and orientation (Example: incident, Y, 45 degrees CCW, scattered, N)")
    data_processing: Optional[Set[str]] = Field(None, description="Data manipulation")

    class Config:
        title = "Measurement parameters"


class RamanResults(BaseModel):
    identified_components: Set[str] = Field(None, title='Identified components')
    comments: Optional[str] = Field(None, title='Comments', description='Comments with regards to generated research data')

    class Config:
        title = "Measurement results"


class Raman(Measurement):
    dataset_type: str = Field("raman", const=True) #OVERRIDE FROM DATASET
    measurement_parameters: Optional[RamanParameters] = Field(None)
    measurement_results: Optional[RamanResults] = Field(None)

    class Config:
        title = "Micro-Raman Spectrometry"

