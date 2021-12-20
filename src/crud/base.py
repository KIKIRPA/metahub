from typing import List
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
import pymongo.errors


def translate_id(obj: dict):
    if obj is not None:
        id = obj.pop("_id")
        obj["id"] = str(id)
        return obj
    else:
        return None


class NoResultsError(Exception):
    pass


class NotCreatedError(Exception):
    pass


class NotUpdatedError(Exception):
    pass


class NotDeletedError(Exception):
    pass


class DuplicateKeyError(Exception):
    pass


class CRUDBase():
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """

    async def get(
            self, 
            collection: AsyncIOMotorCollection, 
            *,
            id: str) -> dict:
        result = await collection.find_one({"_id": ObjectId(id)})
        if result is None: raise NoResultsError
        return translate_id(result)


    async def get_all(
            self, 
            collection: AsyncIOMotorCollection, 
            sort_by: List[str] = [],
            sort_desc: List[bool] = [],
            skip: int = 0, 
            limit: int = 10) -> dict:
        pagination = {
            "skip": skip,
            "limit": limit,
            "total": await collection.count_documents({})
        }
        if limit < 0: limit = 0
        if len(sort_by) > 0:
            sort = []
            for i in range(len(sort_by)):
                if len(sort_desc) == len(sort_by):
                    sort.append((sort_by[i], -1 if sort_desc[i] == True else 1))
                else:
                    sort.append((sort_by[i], 1))
            data = await collection.find({}).sort(sort).skip(skip).limit(limit).to_list(None)
            pagination["sort_by"] = sort_by
            if len(sort_desc) > 0 and len(sort_desc) == len(sort_by) :
                pagination["sort_desc"] = sort_desc
        else:
            data = await collection.find({}).skip(skip).limit(limit).to_list(None)
        for doc in data:
            doc = translate_id(doc)
        result = {"pagination": pagination, "data": data}
        return result


    async def create(
            self, 
            collection: AsyncIOMotorCollection, 
            *, 
            data: dict) -> dict:
        data = jsonable_encoder(data)
        try: 
            insert = await collection.insert_one(data)
        except pymongo.errors.DuplicateKeyError:
            raise DuplicateKeyError
        result = await collection.find_one({"_id": insert.inserted_id})
        if result is None: raise NotCreatedError
        return translate_id(result)


    async def update(
            self,
            collection: AsyncIOMotorCollection,
            id: str,
            *,
            data: dict) -> dict:
        result = await collection.find_one({"_id": ObjectId(id)})
        if result is None: raise NoResultsError
        data = jsonable_encoder(data)
        try:
            update = await collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        except pymongo.errors.DuplicateKeyError:
            raise DuplicateKeyError
        if update.modified_count != 1: raise NotUpdatedError
        result = await collection.find_one({"_id": ObjectId(id)})
        if result is None: raise NoResultsError
        return translate_id(result)
    

    async def remove(
            self,
            collection: AsyncIOMotorCollection,
            *,
            id: str)-> dict:
        result = await collection.find_one({"_id": ObjectId(id)})
        if result is None: raise NoResultsError
        delete = await collection.delete_one({"_id": ObjectId(id)})
        if delete.deleted_count != 1: raise NotDeletedError
        return translate_id(result)