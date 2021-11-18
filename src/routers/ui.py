from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Optional

from models.measurement import Measurement
from models.drms import DRMS

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="",
    tags=["ui"]
)

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@router.get("/form", response_class=HTMLResponse)
async def show_form(request: Request, layout: Optional[str] = "jsoneditor"):
    """Displaying document input form
    """
    
    if layout not in ["jsoneditor", "alpaca"]:
        raise HTTPException(status_code=404, detail="Layout does not exist")
    
    schema = Measurement.schema_json(indent=4)
    return templates.TemplateResponse(layout+".html.jinja", {"request": request, "schema": schema})