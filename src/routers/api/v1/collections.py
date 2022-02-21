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
    prefix="/api/v1/collections",
    tags=["api/v1/collections"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


#
#   DATASET ROUTES
#

@router.get("")
async def search_collections(
        skip: Optional[int] = Query(0, description="Skip the x first results"),
        limit: Optional[int] = Query(10, description="Return x results"), 
        find: Optional[str] = Query(None, description="Mongodb-style find query in JSON"),
        sort_by: Optional[List[str]] = Query(["collection_code"], description="Sorting options (array of strings)"),
        sort_desc: Optional[List[bool]] = Query([], description="Sort descending (arry of booleans)")):
    """
    Return all collections.
    """

    if find is not None:
        find = json.loads(find)
    else:
        find = {}

    if len(sort_desc) > 0 and len(sort_desc) != len(sort_by):
        raise HTTPException(status_code=422, detail="Unequal number of items in sort_by and sort_desc")
    try: 
        response = await crud.collection.search(
            collection=db.collections,
            find=find,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_desc=sort_desc)
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.get("/{id}")
async def get_collection_by_id(
        id: str = Path(None, description="The id of the collection")):
    """
    Return a single collection by its id.
    """
    try:
        response = await crud.collection.get(
            collection=db.collections, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="collection not found")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.post("")
async def create_collection(collection: dict):
    """
    Create a new collection.
    """
    try:
        # validate agains resource and category models
        collection_resource_instance = models.DatasetUpdate(**collection)
        await core.utils.jsonschema.validate_instance(collection, validate_category=True)

        # create the collection
        response = await crud.collection.create(
            collection=db.collections,
            data=collection)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.errors())
    except core.utils.jsonschema.SchemaValidationError as err:
        raise HTTPException(status_code=422, detail=err.args[0])
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="duplicate key (collection code)")
    except crud.NotCreatedError:
        raise HTTPException(status_code=400, detail="collection was not created")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response


@router.put("/{id}")
async def replace_collection(
        collection: dict,
        id: str = Path(None, description="The id of the collection")):
    """
    Replace a collection (full update).
    """
    try:
        # validate agains resource and category models
        collection_resource_instance = models.DatasetUpdate(**collection)
        await core.utils.jsonschema.validate_instance(collection, validate_category=True)

        # update the collection
        updated = await crud.collection.replace(
            collection=db.collections, 
            id=id,
            data=collection)
    except ValidationError as err:
        raise HTTPException(status_code=422, detail=err.errors())
    except core.utils.jsonschema.SchemaValidationError as err:
        raise HTTPException(status_code=422, detail=err.args[0])
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="collection not found")
    except crud.DuplicateKeyError:
        raise HTTPException(status_code=422, detail="duplicate key (collection code)")
    except crud.NotUpdatedError:
        raise HTTPException(status_code=400, detail="collection was not updated")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return updated


@router.delete("/{id}")
async def delete_collection(
        id: str = Path(None, description="The id of the collection")):
    """
    Delete a collection.
    """
    try:
        deleted = await crud.collection.remove(
            collection=db.collections, 
            id=id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="collection not found")
    except crud.NotDeletedError:
        raise HTTPException(status_code=400, detail="collection was not deleted")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return deleted