from pydantic import BaseModel

from .measurement import Measurement


class Grating(BaseModel):
    grating_type: str
    grating_density: int


class LaserPower(BaseModel):
    laser_power_at_sample: float
    neutral_density_filtering: float


class RejectionFilters(BaseModel):
    filter_type: str
    cutoff_frequency: float


class SpectralRange(BaseModel):
    spectral_range_low: float
    spectral_range_high: float


class Raman(Measurement):
    instrument: str
    software: str
    detector_type: str
    instrument_class: str
    accessory: str
    excitation_source: float
    laser_power: LaserPower
    spectral_range: SpectralRange
    filters: RejectionFilters
    grating: Grating
    resolution: float
    laser_defocus: bool
    data_collection: str
    integration_time: float
    accumulations: int
    objective: str
    spot_size: float
    confocality: bool
    polarization: str
    baseline_correction: bool
    fluorescence_correction: bool
    cosmic_ray_removal: bool
    detector_binning: bool
    other_data_processing: str
