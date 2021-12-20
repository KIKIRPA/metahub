from typing import Optional, List

from fastapi import APIRouter, HTTPException, status, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient

import config
import models
import models.activities
import models.document_templates
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/v1",
    tags=["api/v1"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(config.settings.mongo_conn_str)
db = client[config.settings.mongo_db]


#
#   TEMPLATES
#

@router.get("/template", response_model=models.TemplateList)
async def get_all_templates(
    skip: Optional[int] = Query(0),
    limit: Optional[int] = Query(10), 
    sort_by: Optional[List[str]] = Query(["category", "schema_id", "template_id"]),
    sort_desc: Optional[List[bool]] = Query([])):
    """
    Return all templates.
    """
    if len(sort_desc) > 0 and len(sort_desc) != len(sort_by):
        raise HTTPException(status_code=422, detail="Unequal number of items in sort_by and sort_desc")
    try: 
        response = await crud.template.get_all(
            collection=db[config.settings.templates_collection],
            skip=skip,
            limit=limit,
            sort_by=sort_by)
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return response


@router.get("/template/{id}", response_model=models.Template)
async def get_template_by_id(
        id: str = Path(None, description="The id of the template")):
    """
    Return a single template by its id.
    """
    try:
        response = await crud.template.get(
            collection=db[config.settings.templates_collection], 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="template not found")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return response


@router.post("/template", response_model=models.Template)
async def create_template(template: models.TemplateUpdate):
    """
    Create a new template.
    """
    try:
        response = await crud.template.create(
            collection=db[config.settings.templates_collection],
            data=template)
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="duplicate key (category, schema_id, template_id)")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="template was not created")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return response


@router.put("/template/{id}", response_model=models.Template)
async def update_template(
        template: models.TemplateUpdate,
        id: str = Path(None, description="The id of the template")):
    """
    Update a template.
    """
    try:
        updated = await crud.template.update(
            collection=db[config.settings.templates_collection], 
            id=id,
            data=template)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="template not found")
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="duplicate key (category, schema_id, template_id)")
    except crud.NotUpdatedError:
        raise HTTPException(status_code=400, detail="template was not updated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return updated


@router.delete("/template/{id}", response_model=models.Template)
async def delete_template(
        id: str = Path(None, description="The id of the template")):
    """
    Delete a template.
    """
    try:
        deleted = await crud.template.remove(
            collection=db[config.settings.templates_collection], 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="template not found")
    except crud.NotDeletedError:
        raise HTTPException(status_code=400, detail="template was not deleted")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return deleted


# OLD ENDPOINT
# @router.get("/template/{document_type}", response_model=List[models.document_templates.DocumentTemplateReduced])
# async def read_templates(document_type: str = Path(None, description="The type of report or measurement")):
#     """
#     Return the JSON schema templates in the db for a given document type.
#     """

#     response = await db[config.settings.templates_collection].find({"schemas": document_type}).to_list(20)

#     return response


#
#   ACTIVITIES
#

@router.get("/activity", response_model=dict)
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
        collection=db[config.settings.activities_collection],
        skip=skip,
        limit=limit,
        sort_by=sort_by)
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
    Delete an activity.
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