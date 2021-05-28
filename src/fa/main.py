from fastapi import FastAPI

from .routers import strict

app = FastAPI()
app.include_router(strict.router)