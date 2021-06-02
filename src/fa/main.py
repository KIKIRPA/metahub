from fastapi import FastAPI

from .routers import strict

# Main API application
app = FastAPI()
# Adding some routes to our main application
app.include_router(strict.router)