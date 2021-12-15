import json
from typing import Optional

from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.param_functions import Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient

import config
import models

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="",
    tags=["ui"]
)

templates = Jinja2Templates(directory="templates")
document_types_list = json.dumps([{"alias": k, "short": v["short"]} for k, v in config.document_types.items()])
activity_types_list = json.dumps([{"alias": k, "name": v["name"]} for k, v in config.activity_types.items()])


@router.get("/activity", response_class=HTMLResponse)
def show_activity_list(request: Request):
    """
    Displaying the activity list
    """
    return templates.TemplateResponse("activity_list.html.jinja", {"request": request})


@router.get("/activity/{activity_type}", response_class=HTMLResponse)
def show_activity_list(
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


@router.get("/config/schema_editor", response_class=HTMLResponse)
def show_activity_list(request: Request):
    """
    Displaying schema editor
    """
    return templates.TemplateResponse("schema_editor.html.jinja", {
        "request": request,
        "schema": models.Template.schema_json()})
