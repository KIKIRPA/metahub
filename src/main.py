from fastapi import FastAPI

from routers import api, schemas

# Main API application
app = FastAPI()
# Adding some routes to our main application
app.include_router(api.router)
app.include_router(schemas.router)