from fastapi import FastAPI

from routers import measurements

# Main API application
app = FastAPI()
# Adding some routes to our main application
app.include_router(measurements.router)