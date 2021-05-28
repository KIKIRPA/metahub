from .measurement import Measurement


class DRMS(Measurement):
    instrument: str
    software: str
    drill_type: str
    radius: float
    rotation_speed: int
    penetration_rate: int
