from typing import Optional, List

from fastapi import APIRouter, HTTPException, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient

import core
import models.activities
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/v1/activities",
    tags=["api/v1/activities"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


@router.get("/", response_model=dict)
async def get_all_activities(
    skip: Optional[int] = Query(0),
    limit: Optional[int] = Query(10), 
    sort_by: Optional[List[str]] = Query(["activity_id", "unit"]),
    sort_desc: Optional[List[bool]] = Query([])):
    """
    Return all activities.
    """
    if len(sort_desc) > 0 and len(sort_desc) != len(sort_by):
        raise HTTPException(status_code=422, detail="Unequal number of items in sort_by and sort_desc")
    response = await crud.activity.get_all(
        collection=db[core.settings.activities_collection],
        skip=skip,
        limit=limit,
        sort_by=sort_by)
    return response


@router.get("/{id}", response_model=models.activities.Activity)
async def get_activity_by_id(
        id: str = Path(None, description="The id of the activity")):
    """
    Return a single activity by its id.
    """
    response = await crud.activity.get(
        collection=db[core.settings.activities_collection], 
        id=id)
    if response is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return response


@router.post("/", response_model=models.activities.Activity)
async def create_activity(activity: models.activities.Activity):
    """
    Create a new activity.
    """
    response = await crud.activity.create(
        collection=db[core.settings.activities_collection],
        data=activity)
    return response


@router.put("/{id}", response_model=models.activities.Activity)
async def update_activity(
        activity: models.activities.Activity,
        id: str = Path(None, description="The id of the activity")):
    """
    Update an activity.
    """
    activity_from_db = await crud.activity.get(
        collection=db[core.settings.activities_collection], 
        id=id)
    if activity_from_db is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    updated = await crud.activity.update(
        collection=db[core.settings.activities_collection], 
        id=id,
        data=activity)
    if not updated:
        raise HTTPException(status_code=400, detail="Bad request")
    return activity


@router.delete("/{id}", response_model=models.activities.Activity)
async def delete_activity(
        id: str = Path(None, description="The id of the activity")):
    """
    Delete an activity.
    """
    activity = await crud.activity.get(
        collection=db[core.settings.activities_collection], 
        id=id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    deleted = await crud.activity.remove(
        collection=db[core.settings.activities_collection], 
        id=id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Bad request")
    return activity