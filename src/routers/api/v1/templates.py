from typing import Optional, List

from fastapi import APIRouter, HTTPException, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient

import config
import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/v1/templates",
    tags=["api/v1/templates"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(config.settings.mongo_conn_str)
db = client[config.settings.mongo_db]


#
#   TEMPLATES
#

@router.get("/", response_model=models.TemplateList)
async def get_all_templates(
    skip: Optional[int] = Query(0),
    limit: Optional[int] = Query(10), 
    sort_by: Optional[List[str]] = Query(["resource", "category", "template"]),
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


@router.get("/{id}", response_model=models.Template)
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


@router.post("/", response_model=models.Template)
async def create_template(template: models.TemplateUpdate):
    """
    Create a new template.
    """
    try:
        response = await crud.template.create(
            collection=db[config.settings.templates_collection],
            data=template)
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="duplicate key (resource, category, template)")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="template was not created")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return response


@router.put("/{id}", response_model=models.Template)
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
        raise HTTPException(status_code=422, detail="duplicate key (resource, category, template)")
    except crud.NotUpdatedError:
        raise HTTPException(status_code=400, detail="template was not updated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return updated


@router.delete("/{id}", response_model=models.Template)
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