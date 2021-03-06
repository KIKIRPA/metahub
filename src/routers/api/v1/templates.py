from typing import Optional, List

from fastapi import APIRouter, HTTPException, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient

import core
import core.utils.jsonschema
from core.enums import Resource
import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/v1/templates",
    tags=["api/v1/templates"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


#
#   TEMPLATE ROUTES
#

@router.get("", response_model=models.TemplateList)
async def search_templates(
        skip: Optional[int] = Query(0, description="Skip the x first results"),
        limit: Optional[int] = Query(10, description="Return x results"), 
        sort_by: Optional[List[str]] = Query(["resource", "category", "template"], description="Sorting options (array of strings)"),
        sort_desc: Optional[List[bool]] = Query([], description="Sort descending (arry of booleans)"),
        resource: Optional[Resource] = Query(None, description="Filter on resource type"),
        category: Optional[str] = Query(None, description="Filter on category identifier (partial match)"),
        template: Optional[str] = Query(None, description="Filter on template identifier (partial match)")):
    """
    Return all templates.
    """
    find = {}
    if resource is not None: find['resource'] = resource
    if category is not None: find['category'] = {'$regex': f'.*{category.lower()}.*'}
    if template is not None: find['template'] = {'$regex': f'.*{template.lower()}.*'}
 
    if len(sort_desc) > 0 and len(sort_desc) != len(sort_by):
        raise HTTPException(status_code=400, detail="ParameterError")
    try: 
        response = await crud.template.search(
            collection=db.templates,
            find=find,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc)
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{id}", response_model=models.Template)
async def get_template_by_id(
        id: str = Path(None, description="The id of the template")):
    """
    Return a single template by its id.
    """
    try:
        response = await crud.template.get(
            collection=db.templates, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="template not found")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{resource}/{category}", response_model=models.Template)
async def get_default_template_by_keys(
        resource: Resource = Path(None, description="Resource of the data described in the template"),
        category: str = Path(None, description="Category of the data described in the template")):
    """
    Return a single template by its keys (template=_default).
    """
    try:
        response = await crud.template.get_by_keys(
            collection=db.templates, 
            resource=resource,
            category=category)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="template not found")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{resource}/{category}/{template}", response_model=models.Template)
async def get_template_by_keys(
        resource: Resource = Path(None, description="Resource of the data described in the template"),
        category: str = Path(None, description="Category of the data described in the template"),
        template: str = Path("_default", description="Template name")):
    """
    Return a single template by its keys.
    """
    try:
        response = await crud.template.get_by_keys(
            collection=db.templates, 
            resource=resource,
            category=category,
            template=template)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="template not found")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("", response_model=models.Template)
async def create_template(template: models.TemplateUpdate):
    """
    Create a new template.
    """
    try:
        # first validate the schema
        resolved_schema = await core.utils.jsonschema.resolve_schema(temporary_template=template)
        core.utils.jsonschema.validate_schema(resolved_schema)

        # create the template
        response = await crud.template.create(
            collection=db.templates,
            data=template)

        # clear the cached data
        core.utils.jsonschema.get_template_list.cache_clear()

    except core.utils.jsonschema.SchemaValidationError as err:
        raise HTTPException(status_code=422, detail=err.args[0])
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="duplicate key (resource, category, template)")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="template was not created")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.put("/{id}", response_model=models.Template)
async def replace_template(
        template: models.TemplateUpdate,
        id: str = Path(None, description="The id of the template")):
    """
    Replace a template (full update).
    """
    try:
        # first validate the schema
        resolved_schema = await core.utils.jsonschema.resolve_schema(temporary_template=template)
        core.utils.jsonschema.validate_schema(resolved_schema)

        # update the template
        updated = await crud.template.replace(
            collection=db.templates, 
            id=id,
            data=template)

        # clear the cached data
        core.utils.jsonschema.get_template_list.cache_clear()

    except core.utils.jsonschema.SchemaValidationError as err:
        raise HTTPException(status_code=422, detail=err.args[0])
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="template not found")
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="duplicate key (resource, category, template)")
    except crud.NotUpdatedError:
        raise HTTPException(status_code=400, detail="template was not updated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return updated


@router.delete("/{id}", response_model=models.Template)
async def delete_template(
        id: str = Path(None, description="The id of the template")):
    """
    Delete a template.
    """
    try:
        deleted = await crud.template.remove(
            collection=db.templates, 
            id=id)
        
        # clear the cached data
        core.utils.jsonschema.get_template_list.cache_clear()
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="template not found")
    except crud.NotDeletedError:
        raise HTTPException(status_code=400, detail="template was not deleted")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return deleted


@router.post("/validate")
async def validate_template(template: models.TemplateUpdate):
    """
    Validate a template.
    """
    try:
        resolved_schema = await core.utils.jsonschema.resolve_schema(temporary_template=template)
        core.utils.jsonschema.validate_schema(resolved_schema)
    except core.utils.jsonschema.SchemaValidationError as err:
        raise HTTPException(status_code=422, detail=err.args[0])
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))

    return resolved_schema