import json
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.param_functions import Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient

import core
from core.enums import Resource
import models
import crud

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="",
    tags=["ui"]
)

templates = Jinja2Templates(directory="templates")
dataset_types_list = json.dumps([{"alias": k, "short": v["short"]} for k, v in core.dataset_types.items()])
project_types_list = json.dumps([{"alias": k, "name": v["name"]} for k, v in core.project_types.items()])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


@router.get("/", response_class=HTMLResponse)
def show_root_page(request: Request):
    """
    Displaying the root page
    """
    return templates.TemplateResponse("root.html.jinja", {"request": request})


@router.get("/templates", response_class=HTMLResponse)
def show_template_list(request: Request):
    """
    Displaying the template list
    """
    return templates.TemplateResponse("template_list.html.jinja", {"request": request})


@router.get("/templates/new", response_class=HTMLResponse)
def show_template_form_new(request: Request):
    """
    Displaying template form for new data entry
    """
    return templates.TemplateResponse("template_form.html.jinja", {
        "request": request,
        "schema": models.TemplateUpdate.schema_json(),
        "id": ""
    })


@router.get("/templates/{template_id}", response_class=HTMLResponse)
def show_template_form_with_id(
        request: Request, 
        template_id: str = Path(None, description="Template identifier")):
    """
    Displaying template form by its id
    """
    return templates.TemplateResponse("template_form.html.jinja", {
        "request": request,
        "schema": models.TemplateUpdate.schema_json(),
        "id": template_id
    })


@router.get("/templates/{resource}/{category}", response_class=HTMLResponse)
async def show_default_template_form_with_keys(
        request: Request,
        resource: Resource = Path(None, description="Resource of the data described in the template"),
        category: str = Path(None, description="Category of the data described in the template")):
    """
    Displaying the default form with given resource and category
    """
    try:
        response = await crud.template.get_by_keys(
            collection=db.templates, 
            resource=resource,
            category=category,
            template="_default")
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="template not found")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)

    return templates.TemplateResponse("template_form.html.jinja", {
        "request": request,
        "schema": models.TemplateUpdate.schema_json(),
        "id": response["id"]})


@router.get("/templates/{resource}/{category}/{template}", response_class=HTMLResponse)
async def show_template_form_with_keys(
        request: Request,
        resource: Resource = Path(None, description="Resource of the data described in the template"),
        category: str = Path(None, description="Category of the data described in the template"),
        template: str = Path("_default", description="Template name")):
    """
    Displaying the form for the template with given resource, category and template 
    """
    try:
        response = await crud.template.get_by_keys(
            collection=db.templates, 
            resource=resource,
            category=category,
            template=template)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="template not found")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)

    return templates.TemplateResponse("template_form.html.jinja", {
        "request": request,
        "schema": models.TemplateUpdate.schema_json(),
        "id": response["id"]})


@router.get("/projects", response_class=HTMLResponse)
def show_project_list(request: Request):
    """
    Displaying the project list
    """
    return templates.TemplateResponse("project_list.html.jinja", {"request": request})







@router.get("/project/{project_type}", response_class=HTMLResponse)
def show_project_form(
        request: Request, 
        project_type: str = Path(None, description="The type of project"),
        id: Optional[str] = Query(None, description="The project id")):
    """
    Displaying the project input form
    """
    
    if project_type not in core.project_types:
        raise HTTPException(status_code=404, detail="Project type does not exist")
    
    return templates.TemplateResponse("project_form.html.jinja", {
        "request": request, 
        "schema_alias": project_type, 
        "template_alias": "",
        "schema_list": project_types_list,
        "id": id 
    })


@router.get("/dataset/{dataset_type}", response_class=HTMLResponse)
async def show_form(
        request: Request, 
        dataset_type: str = Path(None, description="The type of report or measurement")):
    """
    Displaying the dataset input form
    """
    
    if dataset_type not in core.dataset_types:
        raise HTTPException(status_code=404, detail="Dataset type does not exist")
    
    return templates.TemplateResponse("dataset_form.html.jinja", {
        "request": request, 
        "schema_alias": dataset_type, 
        "template_alias": "",
        "schema_list": dataset_types_list
    })


@router.get("/dataset/{dataset_type}/{template}", response_class=HTMLResponse)
async def show_form(
        request: Request, 
        dataset_type: str = Path(None, description="The type of report or measurement"),
        template: str = Path(None, description="Schema template to be applied")):
    """
    Displaying the dataset input form
    """
    
    if dataset_type not in core.dataset_types:
        raise HTTPException(status_code=404, detail="Dataset type does not exist")
    
    client = AsyncIOMotorClient(core.settings.mongo_conn_str)
    db = client[core.settings.mongo_db]

    if (response := await db.templates.find_one({"alias": template, "schemas": dataset_type})) is None:
        raise HTTPException(status_code=404, detail="Template type does not exist (for the given dataset type)")
    
    return templates.TemplateResponse("dataset_form.html.jinja", {
        "request": request, 
        "schema_alias": dataset_type, 
        "template_alias": response["alias"],
        "schema_list": dataset_types_list
    })