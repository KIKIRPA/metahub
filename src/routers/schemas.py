from datetime import date
import os
from typing import List

from fastapi import APIRouter, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import motor.motor_asyncio

from models.measurement import Measurement
from models.drms import DRMS

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/schemas",
    tags=["schemas"]
)


@router.get("/measurement")
async def read_measurement_schema():
    """Displaying json-schema.
    """
    return Measurement.schema_json()

