import json
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.param_functions import Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient

import config
import models
import crud

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="",
    tags=["ui"]
)

templates = Jinja2Templates(directory="templates")
document_types_list = json.dumps([{"alias": k, "short": v["short"]} for k, v in config.document_types.items()])
activity_types_list = json.dumps([{"alias": k, "name": v["name"]} for k, v in config.activity_types.items()])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(config.settings.mongo_conn_str)
db = client[config.settings.mongo_db]


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
        resource: models.Resource = Path(None, description="Resource of the data described in the template"),
        category: str = Path(None, description="Category of the data described in the template")):
    """
    Displaying the default form with given resource and category
    """
    try:
        response = await crud.template.get_by_keys(
            collection=db[config.settings.templates_collection], 
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
        resource: models.Resource = Path(None, description="Resource of the data described in the template"),
        category: str = Path(None, description="Category of the data described in the template"),
        template: str = Path("_default", description="Template name")):
    """
    Displaying the form for the template with given resource, category and template 
    """
    try:
        response = await crud.template.get_by_keys(
            collection=db[config.settings.templates_collection], 
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







@router.get("/activity", response_class=HTMLResponse)
def show_activity_list(request: Request):
    """
    Displaying the activity list
    """
    return templates.TemplateResponse("activity_list.html.jinja", {"request": request})


@router.get("/activity/{activity_type}", response_class=HTMLResponse)
def show_activity_form(
        request: Request, 
        activity_type: str = Path(None, description="The type of activity"),
        id: Optional[str] = Query(None, description="The activity id")):
    """
    Displaying the activity input form
    """
    
    if activity_type not in config.activity_types:
        raise HTTPException(status_code=404, detail="Activity type does not exist")
    
    return templates.TemplateResponse("activity_form.html.jinja", {
        "request": request, 
        "schema_alias": activity_type, 
        "template_alias": "",
        "schema_list": activity_types_list,
        "id": id 
    })


@router.get("/document/{document_type}", response_class=HTMLResponse)
async def show_form(
        request: Request, 
        document_type: str = Path(None, description="The type of report or measurement")):
    """
    Displaying the document input form
    """
    
    if document_type not in config.document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")
    
    return templates.TemplateResponse("document_form.html.jinja", {
        "request": request, 
        "schema_alias": document_type, 
        "template_alias": "",
        "schema_list": document_types_list
    })


@router.get("/document/{document_type}/{template}", response_class=HTMLResponse)
async def show_form(
        request: Request, 
        document_type: str = Path(None, description="The type of report or measurement"),
        template: str = Path(None, description="Schema template to be applied")):
    """
    Displaying the document input form
    """
    
    if document_type not in config.document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")
    
    client = AsyncIOMotorClient(config.settings.mongo_conn_str)
    db = client[config.settings.mongo_db]

    if (response := await db[config.settings.templates_collection].find_one({"alias": template, "schemas": document_type})) is None:
        raise HTTPException(status_code=404, detail="Template type does not exist (for the given document type)")
    
    return templates.TemplateResponse("document_form.html.jinja", {
        "request": request, 
        "schema_alias": document_type, 
        "template_alias": response["alias"],
        "schema_list": document_types_list
    })