from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import routers
import routers.api.v1

# Main API application
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Adding some routes to our main application
app.include_router(routers.api.v1.templates.router)
app.include_router(routers.api.v1.activities.router)
app.include_router(routers.schema.router)
app.include_router(routers.ui.router)