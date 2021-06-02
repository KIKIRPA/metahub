from datetime import date
import os
from typing import List

from fastapi import APIRouter
import motor.motor_asyncio

from ..strict.measurement import Measurement, MeasurementId, Sample
from ..strict.drms import DRMS

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/measurements",
    tags=["strict", "measurements"]
)

# Creating a MongoDB client by using the environment variable MONGODB_URL and
# defaulting to the MongoDB instance created with docker in the 'mongo_container'
client = motor.motor_asyncio.AsyncIOMotorClient(
    os.getenv("MONGODB_URL", "mongodb://kikirpa:hescida@localhost:27017/")
)
# Connecting to the 'strict' database in MongoDB, which was created by hand
db = client.strict

db_measurements = [
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

db_drms = [
    DRMS(
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
        ],
        instrument="instrument",
        software="software",
        drill_type="type",
        radius=0.8,
        rotation_speed=200,
        penetration_rate=100,
    ),
    DRMS(
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
        ],
        instrument="instrument",
        software="software",
        drill_type="type",
        radius=0.75,
        rotation_speed=100,
        penetration_rate=50,
    )
]


@router.get("/", response_model=List[Measurement])
async def read_measurements():
    return db_measurements


@router.get("/drms/", response_model=List[DRMS])
async def read_drms():
    return db_drms
