from fastapi import APIRouter, Request, HTTPException, Path
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Optional

from models.document_types import document_types

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
    document_type: str = Path(None, description="The type of report or measurement"),
    layout: Optional[str] = "jsoneditor"
    ):
    """Displaying document input form
    """
    
    if document_type not in document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")

    if layout not in ["jsoneditor", "alpaca", "vjsf"]:
        raise HTTPException(status_code=404, detail="Layout does not exist")
    
    schema = document_types[document_type]["model"].schema_json(indent=4)
    return templates.TemplateResponse(layout+".html.jinja", {"request": request, "schema": schema})