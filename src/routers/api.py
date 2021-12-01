from functools import lru_cache
from datetime import date
import os
from typing import List

from fastapi import APIRouter, HTTPException, status, Body, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import motor.motor_asyncio

from config import Settings
from models.document_template import DocumentTemplate
from models.measurement import Measurement
from models.drms import DRMS

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api",
    tags=["api"]
)

# Get config settings
@lru_cache()
def get_settings():
    return Settings()

config = get_settings()

# Creating a MongoDB client and connect to the relevant collections
client = motor.motor_asyncio.AsyncIOMotorClient(config.mongo_conn_str)
db = client[config.mongo_db]

    
# Connecting to the 'strict' database in MongoDB, which was created by hand
#db = client.strict

""" 
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
] """


@router.get("/measurements", response_model=List[Measurement])
async def read_measurements():
    """Displaying all measurements in the database.
    """
    measurements = await db["measurements"].find().to_list(1000)
    return measurements


@router.post("/measurements/add", response_model=Measurement)
async def add_measurement(m: Measurement = Body(...)):
    """Adding a Measurement in the database.
    """
    json_data = jsonable_encoder(m)
    new_measurement = await db["measurements"].insert_one(json_data)
    created_measurement = await db["measurements"].find_one(
        {"_id": new_measurement.inserted_id}
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=created_measurement
    )


@router.get("/measurements/add_them_all", response_model=List[Measurement])
async def add_measurements():
    """Populate the MongoDB database with some examples.
    """
    created_measurements = []
    for d in db_measurements:
        m = jsonable_encoder(d)
        new_measurement = await db["measurements"].insert_one(m)
        created_measurement = await db["measurements"].find_one(
            {"_id": new_measurement.inserted_id}
        )
        created_measurements.append(created_measurement)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=created_measurements
    )


@router.get("/drms/", response_model=List[DRMS])
async def read_drms():
    """Displaying the DRMS records in the database.
    """
    return db_drms


@router.get("/template/{document_type}", response_model=List[DocumentTemplate])
async def read_templates(document_type: str = Path(None, description="The type of report or measurement")):
    """
    Return the JSON schema templates in the db for a given document type.
    """

    response = await db[config.templates_collection].find({"schemas": document_type}).to_list(20)

    return response
