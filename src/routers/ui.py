from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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


@router.get("/alpaca", response_class=HTMLResponse)
async def show_measurements_form_alpaca(request: Request):
    """Displaying json-schema.
    """
    return templates.TemplateResponse("alpaca.html", {"request": request})


@router.get("/jsoneditor", response_class=HTMLResponse)
async def show_measurements_form_jsoneditor(request: Request):
    """Displaying json-schema.
    """
    return templates.TemplateResponse("jsoneditor.html", {"request": request})