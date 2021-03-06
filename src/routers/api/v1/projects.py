from typing import Optional, List
import json

from fastapi import APIRouter, HTTPException, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError

import core
import core.utils.jsonschema
import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/v1/projects",
    tags=["api/v1/projects"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


#
#   PROJECT ROUTES
#

@router.get("")
async def search_projects(
        skip: Optional[int] = Query(0, description="Skip the x first results"),
        limit: Optional[int] = Query(10, description="Return x results"), 
        find: Optional[str] = Query(None, description="Mongodb-style find query in JSON"),
        sort_by: Optional[List[str]] = Query(["project_code", "unit"], description="Sorting options (array of strings)"),
        sort_desc: Optional[List[bool]] = Query([], description="Sort descending (arry of booleans)")):
    """
    Return all projects.
    """

    if find is not None:
        find = json.loads(find)
    else:
        find = {}

    if len(sort_desc) > 0 and len(sort_desc) != len(sort_by):
        raise HTTPException(status_code=400, detail="ParameterError")
    try: 
        response = await crud.project.search(
            collection=db.projects,
            find=find,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc)
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/keys")
async def get_project_by_its_unique_keys(
        project_code: str = Query(..., description="Project code (file number, acronym...)"),
        unit: models.Unit = Query(..., description="Unit")):
    """
    Return a single project by its unique keys.
    """
    try:
        response = await crud.project.get_by_keys(
            collection=db.projects,
            project_code=project_code,
            unit=unit)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{id}")
async def get_project_by_id(
        id: str = Path(None, description="The id of the project")):
    """
    Return a single project by its id.
    """
    try:
        response = await crud.project.get(
            collection=db.projects, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("")
async def create_project(project: dict):
    """
    Create a new project.
    """
    try:
        # validate agains resource and category models
        project_resource_instance = models.ProjectUpdate(**project)
        await core.utils.jsonschema.validate_instance(project, validate_category=True)

        # create the project
        response = await crud.project.create(
            collection=db.projects,
            data=project)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.errors())
    except core.utils.jsonschema.SchemaValidationError as err:
        raise HTTPException(status_code=422, detail=err.args[0])
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="NotCreated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.put("/{id}")
async def replace_project(
        project: dict,
        id: str = Path(None, description="The id of the project")):
    """
    Replace a project (full update).
    """
    try:
        # validate agains resource and category models
        project_resource_instance = models.ProjectUpdate(**project)
        await core.utils.jsonschema.validate_instance(project, validate_category=True)

        # update the project
        updated = await crud.project.cascading_replace(
            collection=db.projects, 
            id=id,
            data=project)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.errors())
    except core.utils.jsonschema.SchemaValidationError as err:
        raise HTTPException(status_code=422, detail=err.args[0])
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotUpdatedError:
        raise HTTPException(status_code=400, detail="NotUpdated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return updated


@router.delete("/{id}")
async def delete_project(
        id: str = Path(None, description="The id of the project")):
    """
    Delete a project.
    """
    try:
        deleted = await crud.project.cascading_remove(
            collection=db.projects, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except crud.NotDeletedError:
        raise HTTPException(status_code=400, detail="NotDeleted")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return deleted