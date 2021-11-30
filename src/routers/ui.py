from functools import lru_cache

from fastapi import APIRouter, Request, HTTPException, Path, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import motor.motor_asyncio

from config import Settings
from models.document_types import document_types

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="",
    tags=["ui"]
)

templates = Jinja2Templates(directory="templates")


@lru_cache()
def get_settings():
    return Settings()


@router.get("/{document_type}", response_class=HTMLResponse)
async def show_form(
        request: Request, 
        document_type: str = Path(None, description="The type of report or measurement")):
    """
    Displaying document input form
    """
    
    if document_type not in document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")
    
    #schema = document_types[document_type]["model"].schema_json(indent=4)
    return templates.TemplateResponse("documentForm.html.jinja", {"request": request, "schema": document_type})


@router.get("/{document_type}/{template}", response_class=HTMLResponse)
async def show_form(
        request: Request, 
        document_type: str = Path(None, description="The type of report or measurement"),
        template: str = Path(None, description="Schema template to be applied"),
        config: Settings = Depends(get_settings)):
    """
    Displaying document input form
    """
    
    if document_type not in document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")
    
    client = motor.motor_asyncio.AsyncIOMotorClient(config.mongo_conn_str)
    db = client[config.mongo_db]

    if (response := await db[config.templates_collection].find_one({"alias": template, "schemas": document_type})) is None:
        raise HTTPException(status_code=404, detail="Template type does not exist (for the given document type)")
    
    schema = document_type + '/' + response["alias"]
    return templates.TemplateResponse("documentForm.html.jinja", {"request": request, "schema": schema})
