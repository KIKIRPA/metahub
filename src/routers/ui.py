import json

from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient

import config

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="",
    tags=["ui"]
)

templates = Jinja2Templates(directory="templates")
schema_list = json.dumps([{"alias": k, "short": v["short"]} for k, v in config.document_types.items()])


@router.get("/document/{document_type}", response_class=HTMLResponse)
async def show_form(
        request: Request, 
        document_type: str = Path(None, description="The type of report or measurement")):
    """
    Displaying document input form
    """
    
    if document_type not in config.document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")
    
    return templates.TemplateResponse("documentForm.html.jinja", {
        "request": request, 
        "schema_alias": document_type, 
        "template_alias": "",
        "schema_list": schema_list
    })


@router.get("/document/{document_type}/{template}", response_class=HTMLResponse)
async def show_form(
        request: Request, 
        document_type: str = Path(None, description="The type of report or measurement"),
        template: str = Path(None, description="Schema template to be applied")):
    """
    Displaying document input form
    """
    
    if document_type not in config.document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")
    
    client = AsyncIOMotorClient(config.settings.mongo_conn_str)
    db = client[config.settings.mongo_db]

    if (response := await db[config.settings.templates_collection].find_one({"alias": template, "schemas": document_type})) is None:
        raise HTTPException(status_code=404, detail="Template type does not exist (for the given document type)")
    
    return templates.TemplateResponse("documentForm.html.jinja", {
        "request": request, 
        "schema_alias": document_type, 
        "template_alias": response["alias"],
        "schema_list": schema_list
    })
