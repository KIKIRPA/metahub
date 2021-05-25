from pydantic import BaseModel


class DRMS(BaseModel):
    instrument: str
    software: str
    drill_type: str
    radius: float
    rotation_speed: int
    penetration_rate: int
