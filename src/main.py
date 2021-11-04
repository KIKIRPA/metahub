from fastapi import FastAPI

from routers import measurements, schemas

# Main API application
app = FastAPI()
# Adding some routes to our main application
app.include_router(measurements.router)
app.include_router(schemas.router)