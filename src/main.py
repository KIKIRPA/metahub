from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import api, schemas, ui

# Main API application
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Adding some routes to our main application
app.include_router(api.router)
app.include_router(schemas.router)
app.include_router(ui.router)