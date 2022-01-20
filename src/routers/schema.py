from fastapi import APIRouter, Path
from motor.motor_asyncio import AsyncIOMotorClient

import core
from core.utils import resolve_schema
from core.enums import Resource


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/schema",
    tags=["schema"]
)

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]



@router.get("/{resource}")
async def get_schema_by_resource(
        resource: Resource = Path(None, description="Resource of the data described in the template")):
    """
    Returning a json-schema for a resource.
    """
    return await resolve_schema(resource)


@router.get("/{resource}/{category}")
async def get_schema_by_category(
        resource: Resource = Path(None, description="Resource of the data described in the template"),
        category: str = Path(None, description="Category of the data described in the template")):
    """
    Returning a json-schema for a category.
    """
    return await resolve_schema(resource, category)


@router.get("/{resource}/{category}/{template}")
async def get_schema_by_template(
        resource: Resource = Path(None, description="Resource of the data described in the template"),
        category: str = Path(None, description="Category of the data described in the template"),
        template: str = Path(None, description="Template name")):
    """
    Returning a json-schema for a resource.
    """
    return await resolve_schema(resource, category, template)