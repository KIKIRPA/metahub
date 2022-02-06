from typing import Optional, List

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

@router.get("/")
async def search_projects(
        skip: Optional[int] = Query(0, description="Skip the x first results"),
        limit: Optional[int] = Query(10, description="Return x results"), 
        sort_by: Optional[List[str]] = Query(["project_code", "unit"], description="Sorting options (array of strings)"),
        sort_desc: Optional[List[bool]] = Query([], description="Sort descending (arry of booleans)"),
        category: Optional[str] = Query(None, description="Filter on category identifier (partial match)"),
        template: Optional[str] = Query(None, description="Filter on template identifier (partial match)")):
    """
    Return all projects.
    """
    find = {}
    if category is not None: find['category'] = {'$regex': f'.*{category.lower()}.*'}
    if template is not None: find['template'] = {'$regex': f'.*{template.lower()}.*'}

    if len(sort_desc) > 0 and len(sort_desc) != len(sort_by):
        raise HTTPException(status_code=422, detail="Unequal number of items in sort_by and sort_desc")
    try: 
        response = await crud.project.search(
            collection=db.projects,
            find=find,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc)
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
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
        raise HTTPException(status_code=404, detail="project not found")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return response


@router.post("/")
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
        raise HTTPException(status_code=422, detail="duplicate key (project code, unit)")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="project was not created")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return response


@router.put("/{id}")
async def update_project(
        project: dict,
        id: str = Path(None, description="The id of the project")):
    """
    Update a project.
    """
    try:
        # validate agains resource and category models
        project_resource_instance = models.ProjectUpdate(**project)
        await core.utils.jsonschema.validate_instance(project, validate_category=True)

        # update the project
        updated = await crud.project.update(
            collection=db.projects, 
            id=id,
            data=project)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.errors())
    except core.utils.jsonschema.SchemaValidationError as err:
        raise HTTPException(status_code=422, detail=err.args[0])
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="project not found")
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="duplicate key (project code, unit)")
    except crud.NotUpdatedError:
        raise HTTPException(status_code=400, detail="project was not updated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return updated


@router.delete("/{id}")
async def delete_project(
        id: str = Path(None, description="The id of the project")):
    """
    Delete a project.
    """
    try:
        deleted = await crud.project.remove(
            collection=db.projects, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="project not found")
    except crud.NotDeletedError:
        raise HTTPException(status_code=400, detail="project was not deleted")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return deleted