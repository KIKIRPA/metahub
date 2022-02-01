from typing import Optional, List

from fastapi import APIRouter, HTTPException, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient

import core
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
        sort_by: Optional[List[str]] = Query(["resource", "category", "template"], description="Sorting options (array of strings)"),
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







@router.get("/{id}", response_model=models.projects.Project)
async def get_project_by_id(
        id: str = Path(None, description="The id of the project")):
    """
    Return a single project by its id.
    """
    response = await crud.project.get(
        collection=db.projects, 
        id=id)
    if response is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return response


@router.post("/", response_model=models.projects.Project)
async def create_project(project: models.projects.Project):
    """
    Create a new project.
    """
    response = await crud.project.create(
        collection=db.projects,
        data=project)
    return response


@router.put("/{id}", response_model=models.projects.Project)
async def update_project(
        project: models.projects.Project,
        id: str = Path(None, description="The id of the project")):
    """
    Update an project.
    """
    project_from_db = await crud.project.get(
        collection=db.projects, 
        id=id)
    if project_from_db is None:
        raise HTTPException(status_code=404, detail="Project not found")
    updated = await crud.project.update(
        collection=db.projects, 
        id=id,
        data=project)
    if not updated:
        raise HTTPException(status_code=400, detail="Bad request")
    return project


@router.delete("/{id}", response_model=models.projects.Project)
async def delete_project(
        id: str = Path(None, description="The id of the project")):
    """
    Delete an project.
    """
    project = await crud.project.get(
        collection=db.projects, 
        id=id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    deleted = await crud.project.remove(
        collection=db.projects, 
        id=id)
    if not deleted:
        raise HTTPException(status_code=400, detail="Bad request")
    return project