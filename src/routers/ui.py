import json
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.param_functions import Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient

import core
from core.enums import Resource
import core.utils.jsonschema
import models
import crud

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="",
    tags=["ui"]
)

templates = Jinja2Templates(directory="templates")

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]



#
#   ROOT PAGE
#

@router.get("/", response_class=HTMLResponse)
def show_root_page(request: Request):
    """
    Displaying the root page
    """
    return templates.TemplateResponse("root.html.jinja", {"request": request})


#
#   TEMPLATES
#

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


#
#   PROJECTS
#

@router.get("/projects", response_class=HTMLResponse)
def show_project_list(request: Request):
    """
    Displaying the project list
    """
    return templates.TemplateResponse("project_list.html.jinja", {"request": request})


@router.get("/projects/new", response_class=HTMLResponse)
async def show_project_form_new(
        request: Request,
        category: Optional[str] = Query(None, description="Project category"),
        template: Optional[str] = Query(None, description="Project template")):
    """
    Displaying project form for new data entry
    """
    template_list = await core.utils.jsonschema.get_template_list("project")
    return templates.TemplateResponse("project_form.html.jinja", {
        "request": request,
        "id": "",
        "category": category if category is not None else "",
        "template": template if template is not None else "",
        "template_list": json.dumps(template_list)
    })


@router.get("/projects/{project_id}", response_class=HTMLResponse)
async def show_project_form_with_id(
        request: Request, 
        project_id: str = Path(None, description="Project identifier")):
    """
    Displaying a project by its id
    """
    template_list = await core.utils.jsonschema.get_template_list("project")
    return templates.TemplateResponse("project_form.html.jinja", {
        "request": request,
        "id": project_id,
        "template_list": json.dumps(template_list)
    })