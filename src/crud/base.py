from typing import Generic, Union, List, Dict, Optional, TypeVar

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorCollection


ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """

    async def get(
            self, 
            collection: AsyncIOMotorCollection, 
            *,
            id: str) -> Optional[ModelType]:
        return await collection.find_one({"_id": id})

    async def get_all(
            self, 
            collection: AsyncIOMotorCollection, 
            sort_by: List[str] = [],
            sort_desc: List[bool] = [],
            skip: int = 0, 
            limit: int = 10) -> List[ModelType]:
        pagination = {
            "skip": skip,
            "limit": limit,
            "total": await collection.count_documents({})
        }
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
        return {"pagination": pagination, "data": data}


    async def create(
            self, 
            collection: AsyncIOMotorCollection, 
            *, 
            data: CreateSchemaType) -> ModelType:
        data = jsonable_encoder(data)
        result = await collection.insert_one(data)
        return await collection.find_one({"_id": result.inserted_id})

    async def update(
            self,
            collection: AsyncIOMotorCollection,
            id: str,
            *,
            data: UpdateSchemaType) -> bool:
        data = jsonable_encoder(data)
        result = await collection.update_one({"_id": id}, {"$set": data})
        return (result.modified_count == 1)
    
    async def remove(
            self,
            collection: AsyncIOMotorCollection,
            *,
            id: str)-> ModelType:
        result = await collection.delete_one({"_id": id})
        return (result.deleted_count == 1)