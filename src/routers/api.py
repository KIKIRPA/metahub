from datetime import date
import os
from typing import List

from fastapi import APIRouter, HTTPException, status, Body, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import motor.motor_asyncio

import config
import models.activities
import models.document_templates

import crud

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/v1",
    tags=["api"]
)

# Creating a MongoDB client and connect to the relevant collections
client = motor.motor_asyncio.AsyncIOMotorClient(config.settings.mongo_conn_str)
db = client[config.settings.mongo_db]


@router.get("/activity", response_model=List[models.activities.Activity])
async def get_all_activities(skip: int = 0, limit: int = 10):
    """
    Return all activities.
    """
    response = await crud.activity.get_all(
        collection=db[config.settings.activities_collection],
        skip=skip,
        limit=limit)
    return response


@router.get("/activity/{id}", response_model=models.activities.Activity)
async def get_activity_by_id(
        id: str = Path(None, description="The id of the activity")):
    """
    Return a single activity by its id.
    """
    response = await crud.activity.get(
        collection=db[config.settings.activities_collection], 
        id=id)
    if response is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return response


@router.post("/activity", response_model=models.activities.Activity)
async def create_activity(activity: models.activities.Activity):
    """
    Create a new activity.
    """
    response = await crud.activity.create(
        collection=db[config.settings.activities_collection],
        data=activity)
    return response


@router.put("/activity/{id}", response_model=models.activities.Activity)
async def update_activity(
        activity: models.activities.Activity,
        id: str = Path(None, description="The id of the activity")):
    """
    Update an activity.
    """
    activity_from_db = await crud.activity.get(
        collection=db[config.settings.activities_collection], 
        id=id)
    if activity_from_db is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    updated = await crud.activity.update(
        collection=db[config.settings.activities_collection], 
        id=id,
        data=activity)
    if not updated:
        raise HTTPException(status_code=400, detail="Bad request")
    return activity


@router.delete("/activity/{id}", response_model=models.activities.Activity)
async def delete_activity(
        id: str = Path(None, description="The id of the activity")):
    """
    Update an activity.
    """
    activity = await crud.activity.get(
        collection=db[config.settings.activities_collection], 
        id=id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    deleted = await crud.activity.remove(
        collection=db[config.settings.activities_collection], 
        id=id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Bad request")
    return activity


# @router.get("/measurements", response_model=List[Measurement])
# async def read_measurements():
#     """Displaying all measurements in the database.
#     """
#     measurements = await db["measurements"].find().to_list(1000)
#     return measurements


# @router.post("/measurements/add", response_model=Measurement)
# async def add_measurement(m: Measurement = Body(...)):
#     """Adding a Measurement in the database.
#     """
#     json_data = jsonable_encoder(m)
#     new_measurement = await db["measurements"].insert_one(json_data)
#     created_measurement = await db["measurements"].find_one(
#         {"_id": new_measurement.inserted_id}
#     )
#     return JSONResponse(
#         status_code=status.HTTP_201_CREATED,
#         content=created_measurement
#     )


# @router.get("/measurements/add_them_all", response_model=List[Measurement])
# async def add_measurements():
#     """Populate the MongoDB database with some examples.
#     """
#     created_measurements = []
#     for d in db_measurements:
#         m = jsonable_encoder(d)
#         new_measurement = await db["measurements"].insert_one(m)
#         created_measurement = await db["measurements"].find_one(
#             {"_id": new_measurement.inserted_id}
#         )
#         created_measurements.append(created_measurement)

#     return JSONResponse(
#         status_code=status.HTTP_201_CREATED,
#         content=created_measurements
#     )


# @router.get("/drms/", response_model=List[DRMS])
# async def read_drms():
#     """Displaying the DRMS records in the database.
#     """
#     return db_drms


@router.get("/template/{document_type}", response_model=List[models.document_templates.DocumentTemplateReduced])
async def read_templates(document_type: str = Path(None, description="The type of report or measurement")):
    """
    Return the JSON schema templates in the db for a given document type.
    """

    response = await db[config.settings.templates_collection].find({"schemas": document_type}).to_list(20)

    return response