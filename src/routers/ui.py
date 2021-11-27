from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.document_types import document_types, test_document_templates

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="",
    tags=["ui"]
)

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


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
        template: str = Path(None, description="Schema template to be applied")):
    """
    Displaying document input form
    """
    
    if document_type not in document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")
    if template not in test_document_templates:
        raise HTTPException(status_code=404, detail="Template type does not exist (for the given document type)")
    
    schema = document_type + '/' + template
    return templates.TemplateResponse("documentForm.html.jinja", {"request": request, "schema": schema})
