from logging import NullHandler
from mergedeep import merge

from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

import core
from core.enums import Resource
from models import Activity, Document, TemplateUpdate
import crud


# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


def get_resource_schema(resource: Resource):
    try: 
        model = resource.value.capitalize()
        schema = globals()[model].schema()
    except:
        raise HTTPException(status_code=404, detail=f"schema not found: '{resource.value}'")
    return schema


async def get_template(resource: Resource, category: str, template: str = "_default"):
    try:
        response = await crud.template.get_by_keys(
            collection=db[core.settings.templates_collection], 
            resource=resource,
            category=category,
            template=template)
    except crud.NoResultsError:
        key = f"{resource.value}/{category}" + f"/{template}" if template != "_default" else ""
        raise HTTPException(status_code=404, detail=f"schema not found: '{key}'")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return response


async def resolve_schema(
        resource: Resource = None, 
        category: str = None, 
        template: str = "_default", 
        temporary_template: TemplateUpdate = None):
    """
    Resolves a schema.
    - With only a resource, returns the schema of the pydantic model for the resource
    - With resource, category and optional template, returns the resolved schema
    - With resource and temporary_template, returns the resolved schema
    """
    t = None
    c = None
    resource_schema = {}
    category_schema = {}
    template_schema = {}
    prevent_inheritance = False
    id_parts = []

    if resource is None and temporary_template is None:
        raise RuntimeError('Invalid arguments for resolve_schema')

    if temporary_template is not None:
        id_parts.append("[unsaved]")
        resource = temporary_template.resource
        category = temporary_template.category
        template = temporary_template.template
        if template != '_default':
            t = temporary_template.dict()
        else:
            c = temporary_template.dict()

    if template != '_default' and category != None:
        if t is None:
            t = await get_template(resource, category, template)
        template_schema = t['json_schema']
        template_schema["title"] = t["title"]
        id_parts.append(template)
        if t['independent_schema']:
            prevent_inheritance = True

    if category != None:
        id_parts.append(category)
        if prevent_inheritance == False:
            if c is None:
                c = await get_template(resource, category)
            category_schema = c['json_schema']
            category_schema["title"] = c["title"]
            if c['independent_schema']:
                prevent_inheritance = True

    id_parts.append(resource.value)
    if prevent_inheritance == False:
        resource_schema = get_resource_schema(resource)
    
    id_base = core.settings.json_schema_base_url
    if id_base[-1] == "/": id_base = id_base[:-1]
    id_parts.append(id_base)
    id_parts.reverse()

    base_schema = {
        "$schema": core.settings.json_schema_version,
        "$id": "/".join(id_parts)
    }

    return merge({}, base_schema, resource_schema, category_schema, template_schema)