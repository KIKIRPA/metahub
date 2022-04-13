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
    prefix="/api/v1/datasets",
    tags=["api/v1/datasets"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


#
#   DATASET ROUTES
#

@router.get("")
async def search_datasets(
        skip: Optional[int] = Query(0, description="Skip the x first results"),
        limit: Optional[int] = Query(10, description="Return x results"), 
        find: Optional[str] = Query(None, description="Mongodb-style find query in JSON"),
        sort_by: Optional[List[str]] = Query(["dataset_code"], description="Sorting options (array of strings)"),
        sort_desc: Optional[List[bool]] = Query([], description="Sort descending (arry of booleans)")):
    """
    Return all datasets.
    """

    if find is not None:
        find = json.loads(find)
    else:
        find = {}

    if len(sort_desc) > 0 and len(sort_desc) != len(sort_by):
        raise HTTPException(status_code=400, detail="ParameterError")
    try: 
        response = await crud.dataset.search(
            collection=db.datasets,
            find=find,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc)
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/keys")
async def get_dataset_by_its_unique_key(
        dataset_code: str = Query(..., description="Dataset code")):
    """
    Return a single dataset by its unique key.
    """
    print(dataset_code)
    try:
        response = await crud.dataset.get_by_keys(
            collection=db.datasets,
            dataset_code=dataset_code)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{id}")
async def get_dataset_by_id(
        id: str = Path(None, description="The id of the dataset")):
    """
    Return a single dataset by its id.
    """
    try:
        response = await crud.dataset.get(
            collection=db.datasets, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("")
async def create_dataset(dataset: dict):
    """
    Create a new dataset.
    """
    try:
        # validate agains resource and category models
        dataset_resource_instance = models.DatasetUpdate(**dataset)
        await core.utils.jsonschema.validate_instance(dataset, validate_category=True)

        # create the dataset
        response = await crud.dataset.create(
            collection=db.datasets,
            data=dataset)
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
async def replace_dataset(
        dataset: dict,
        id: str = Path(None, description="The id of the dataset")):
    """
    Replace a dataset (full update).
    """
    try:
        # validate agains resource and category models
        dataset_resource_instance = models.DatasetUpdate(**dataset)
        await core.utils.jsonschema.validate_instance(dataset, validate_category=True)

        # update the dataset
        updated = await crud.dataset.replace(
            collection=db.datasets, 
            id=id,
            data=dataset)
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
async def delete_dataset(
        id: str = Path(None, description="The id of the dataset")):
    """
    Delete a dataset.
    """
    try:
        deleted = await crud.dataset.remove(
            collection=db.datasets, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except crud.NotDeletedError:
        raise HTTPException(status_code=400, detail="NotDeleted")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return deleted