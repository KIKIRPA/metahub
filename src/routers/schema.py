from mergedeep import merge

from fastapi import APIRouter, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient

import config
from models import Activity, Document, Resource
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/schema",
    tags=["schema"]
)

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(config.settings.mongo_conn_str)
db = client[config.settings.mongo_db]


def get_resource_schema(resource: Resource):
    try: 
        model = resource.value.capitalize()
        schema = globals()[model].schema()
    except:
        raise HTTPException(status_code=404, detail=f"schema not found: '{resource.value}'")
    return schema


async def get_template_schema(resource: Resource, category: str, template: str = "_default"):
    try:
        response = await crud.template.get_by_keys(
            collection=db[config.settings.templates_collection], 
            resource=resource,
            category=category,
            template=template)
        schema = response["json_schema"]
        schema["title"] = response["title"]
    except crud.NoResultsError:
        key = f"{resource.value}/{category}" + f"/{template}" if template != "_default" else ""
        raise HTTPException(status_code=404, detail=f"schema not found: '{key}'")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)

    return schema


@router.get("/{resource}")
def get_schema_by_resource(
        resource: Resource = Path(None, description="Resource of the data described in the template")):
    """
    Returning a json-schema for a resource.
    """
    resource_schema = get_resource_schema(resource)
    base_schema = {
        "$schema": config.settings.json_schema_version,
        "$id": f"https://balat.kikirpa.be/schema/{resource.value}"
    }

    return merge({}, base_schema, resource_schema)


@router.get("/{resource}/{category}")
async def get_schema_by_category(
        resource: Resource = Path(None, description="Resource of the data described in the template"),
        category: str = Path(None, description="Category of the data described in the template")):
    """
    Returning a json-schema for a category.
    """
    resource_schema = get_resource_schema(resource)
    category_schema = await get_template_schema(resource, category)
    base_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": f"https://balat.kikirpa.be/schema/{resource.value}/{category}"
    }

    return merge({}, base_schema, resource_schema, category_schema)


@router.get("/{resource}/{category}/{template}")
async def get_schema_by_template(
        resource: Resource = Path(None, description="Resource of the data described in the template"),
        category: str = Path(None, description="Category of the data described in the template"),
        template: str = Path(None, description="Template name")):
    """
    Returning a json-schema for a resource.
    """
    if template == "_default":
        return await get_schema_by_category(resource, category)

    resource_schema = get_resource_schema(resource)
    category_schema = await get_template_schema(resource, category)
    template_schema = await get_template_schema(resource, category, template)
    base_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "$id": f"https://balat.kikirpa.be/schema/{resource.value}/{category}/{template}"
    }

    return merge({}, base_schema, resource_schema, category_schema, template_schema)