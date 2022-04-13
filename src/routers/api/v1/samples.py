from typing import Optional, List
import json

from fastapi import APIRouter, HTTPException, Query, Path
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError

import core
import core.utils.jsonschema
import models
import crud


# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/v1/samples",
    tags=["api/v1/samples"])

# Creating a MongoDB client and connect to the relevant samples
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


#
#   DATASET ROUTES
#

@router.get("")
async def search_samples(
        skip: Optional[int] = Query(0, description="Skip the x first results"),
        limit: Optional[int] = Query(10, description="Return x results"), 
        find: Optional[str] = Query(None, description="Mongodb-style find query in JSON"),
        sort_by: Optional[List[str]] = Query(["sample_code", "collection_id"], description="Sorting options (array of strings)"),
        sort_desc: Optional[List[bool]] = Query([], description="Sort descending (arry of booleans)")):
    """
    Return all samples.
    """

    if find is not None:
        find = json.loads(find)
    else:
        find = {}

    if len(sort_desc) > 0 and len(sort_desc) != len(sort_by):
        raise HTTPException(status_code=400, detail="ParameterError")
    try: 
        response = await crud.sample.search(
            collection=db.samples,
            find=find,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc)
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/keys")
async def get_sample_by_its_unique_keys(
        sample_code: str = Query(..., description='Sample code'),
        collection_id: str = Query(..., description="Collection Id")):
    """
    Return a single sample by its unique keys.
    """
    try:
        response = await crud.sample.get_by_keys(
            collection=db.samples,
            sample_code=sample_code,
            collection_id=collection_id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{id}")
async def get_sample_by_id(
        id: str = Path(None, description="The id of the sample")):
    """
    Return a single sample by its id.
    """
    try:
        response = await crud.sample.get(
            collection=db.samples, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("")
async def create_sample(sample: dict):
    """
    Create a new sample.
    """
    try:
        # validate agains resource and category models
        sample_resource_instance = models.SampleUpdate(**sample)
        await core.utils.jsonschema.validate_instance(sample, validate_category=True)

        # create the sample
        response = await crud.sample.create(
            collection=db.samples,
            data=sample)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.errors())
    except core.utils.jsonschema.SchemaValidationError as err:
        raise HTTPException(status_code=422, detail=err.args[0])
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="NotCreated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.put("/{id}")
async def replace_sample(
        sample: dict,
        id: str = Path(None, description="The id of the sample")):
    """
    Replace a sample (full update).
    """
    try:
        # validate agains resource and category models
        sample_resource_instance = models.SampleUpdate(**sample)
        await core.utils.jsonschema.validate_instance(sample, validate_category=True)

        # update the sample
        updated = await crud.sample.cascading_replace(
            collection=db.samples, 
            id=id,
            data=sample)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.errors())
    except core.utils.jsonschema.SchemaValidationError as err:
        raise HTTPException(status_code=422, detail=err.args[0])
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="DuplicateKey")
    except crud.NotUpdatedError:
        raise HTTPException(status_code=400, detail="NotUpdated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return updated


@router.delete("/{id}")
async def delete_sample(
        id: str = Path(None, description="The id of the sample")):
    """
    Delete a sample.
    """
    try:
        deleted = await crud.sample.cascading_remove(
            collection=db.samples, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except crud.NotDeletedError:
        raise HTTPException(status_code=400, detail="NotDeleted")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return deleted