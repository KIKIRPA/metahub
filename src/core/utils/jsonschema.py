import asyncstdlib
import jsonschema
from mergedeep import merge
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

import core
from core.enums import Resource, JsonSchemaVersion
from models import (
    Project, ProjectUpdate, 
    Dataset, DatasetUpdate, 
    Collection, CollectionUpdate, 
    Sample, SampleUpdate,
    TemplateUpdate)
import crud


# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


class SchemaValidationError(Exception):
    """
    Exception raised when a JSON schema could not be validated
    (use err.arg[0] to retrieve a dict with the error details)
    """
    pass


def get_keys(schema_url: str):
    if schema_url.startswith(core.settings.json_schema_base_url):
        url_part = schema_url.replace(core.settings.json_schema_base_url, '')
        if url_part.startswith("/"): 
            url_part = url_part[1:]
        keys = url_part.split("/")
        if len(keys) == 2 or len(keys) == 3:
            if len(keys) == 2:
                keys.append("_default")
            keys[0] = keys[0].upper()
            if keys[0] in Resource.__members__:
                keys[0] = Resource[keys[0]]
                return keys
    # if any of the above conditions is not met, raise exception
    detail = {
        "type": "Invalid schema",
        "msg": "Invalid schema",
        "loc": []
    }
    raise SchemaValidationError(detail)


def get_resource_schema(resource: Resource, update_model: bool = False):
    try: 
        model = resource.name.capitalize()
        if update_model:
            model = model + "Update"
        schema = globals()[model].schema()
    except:
        raise HTTPException(status_code=404, detail=f"schema not found: '{resource.value}'")
    return schema


async def get_template(resource: Resource, category: str, template: str = "_default"):
    try:
        response = await crud.template.get_by_keys(
            collection=db.templates, 
            resource=resource,
            category=category,
            template=template)
    except crud.NoResultsError:
        key = f"{resource.value}/{category}" + f"/{template}" if template != "_default" else ""
        raise HTTPException(status_code=404, detail=f"schema not found: '{key}'")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=err)
    return response


@asyncstdlib.lru_cache(maxsize=32)
async def get_template_list(resource: Resource, include_non_selectable: bool = False):
    find = {"resource": resource}

    try:
        response = await crud.template.search(
            collection=db.templates,
            find=find,
            skip=0,
            limit=0,
            sort_by=["category"])
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))

    # select only the required data in a dict, hierarchically structured
    temp = {}
    for item in response["data"]:
        if item["template"] == "_default":
            temp[item["category"]] = {
                "name": item["short_name"],
                "value": item["category"],
                "templates": []
            }
            if include_non_selectable == True or item["selectable"] == True:
                temp[item["category"]]["templates"].append({
                    "name": "(Default)",
                    "value": "_default"
                })
        elif item["category"] in temp:
            if include_non_selectable == True or item["selectable"] == True:
                temp[item["category"]]["templates"].append({
                    "name": item["short_name"],
                    "value": item["template"]
                })

    # remove categories that have zero templates
    available_templates = {}
    for i in temp:
        if len(temp[i]["templates"]) > 0:
            available_templates[i] = temp[i]

    return available_templates


async def resolve_schema(
        resource: Resource = None, 
        category: str = None, 
        template: str = "_default", 
        temporary_template: TemplateUpdate = None,
        update_model: bool = False):
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
        resource_schema = get_resource_schema(resource, update_model)
    
    id_base = core.settings.json_schema_base_url
    if id_base[-1] == "/": id_base = id_base[:-1]
    id_parts.append(id_base)
    id_parts.reverse()

    version = JsonSchemaVersion[core.settings.json_schema_version]
    base_schema = {
        "$schema": version,
        "$id": "/".join(id_parts)
    }

    return merge({}, base_schema, resource_schema, category_schema, template_schema)


def validate_schema(schema: dict):
    # the JSON schema version to validate against is stored in the settings
    version = JsonSchemaVersion[core.settings.json_schema_version]
        
    try:
        if version == JsonSchemaVersion.DRAFT202012:
            jsonschema.Draft201909Validator.check_schema(schema)
        elif version == JsonSchemaVersion.DRAFT201909:
            jsonschema.Draft201909Validator.check_schema(schema)
        elif version == JsonSchemaVersion.DRAFT7:
            jsonschema.Draft7Validator.check_schema(schema)
        elif version == JsonSchemaVersion.DRAFT6:
            jsonschema.Draft6Validator.check_schema(schema)
        elif version == JsonSchemaVersion.DRAFT4:
            jsonschema.Draft4Validator.check_schema(schema)
        elif version == JsonSchemaVersion.DRAFT3:
            jsonschema.Draft3Validator.check_schema(schema)
        else:
            raise NotImplementedError("This draft of JSON-schema is not implemented")
    except jsonschema.exceptions.SchemaError as err:
        detail = {
            "type": f"Invalid JSON Schema: {err.validator} error [{core.settings.json_schema_version}]",
            "msg": err.message,
            "loc": list(err.path)
        }
        raise SchemaValidationError([detail])


async def validate_instance(instance: dict, validate_category=True, validate_template=False):
    if not "$schema" in instance:
        detail = {
            "type": "Missing schema",
            "msg": "Missing schema in instance",
            "loc": []
        }
        raise SchemaValidationError([detail])
    else:
        resource, category, template = get_keys(instance["$schema"])
        if validate_category:
            schema = await resolve_schema(resource, category, update_model=True)
            try:
                jsonschema.validate(instance, schema)
            except jsonschema.exceptions.SchemaError as err:
                detail = {
                    "type": f"Invalid JSON Schema: {err.validator} error [{core.settings.json_schema_version}]",
                    "msg": err.message,
                    "loc": list(err.path)
                }
                raise SchemaValidationError([detail])
            except jsonschema.exceptions.ValidationError as err:
                detail = {
                    "type": f"JSON validator error: {err.validator}",
                    "msg": err.message,
                    "loc": list(err.path)
                }
                raise SchemaValidationError([detail])
        if validate_template and not (validate_category and template == "_default"):
            schema = await resolve_schema(resource, category, template, update_model=True)
            try:
                jsonschema.validate(instance, schema)
            except jsonschema.exceptions.SchemaError as err:
                detail = {
                    "type": f"Invalid JSON Schema: {err.validator} error [{core.settings.json_schema_version}]",
                    "msg": err.message,
                    "loc": list(err.path)
                }
                raise SchemaValidationError([detail])
            except jsonschema.exceptions.ValidationError as err:
                detail = {
                    "type": f"JSON validator error: {err.validator}",
                    "msg": err.message,
                    "loc": list(err.path)
                }
                raise SchemaValidationError([detail])