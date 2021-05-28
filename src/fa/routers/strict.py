from datetime import date
from typing import List

from fastapi import APIRouter

from ..strict.measurement import Measurement, MeasurementId, Sample

router = APIRouter(
    prefix="/measurements",
    tags=["strict", "measurements"]
)

db = [
    Measurement(
        id=MeasurementId(
            technique="technique",
            date=date.today(),
            index=1
        ),
        sample=[
            Sample(id="1", collection="HESCIDA"),
            Sample(id="2", collection="HESCIDA")
        ],
        characteristic="Blah",
        material=[
            "Bois",
            "Fer"
        ]
    ),
    Measurement(
        id=MeasurementId(
            technique="technique",
            date=date.today(),
            index=2
        ),
        sample=[
            Sample(id="3", collection="HESCIDA"),
            Sample(id="4", collection="HESCIDA")
        ],
        characteristic="Blah blah",
        material=[
            "Aluminium",
            "Pierre"
        ]
    )
]


@router.get("/", response_model=List[Measurement])
async def read_measurements():
    return db
