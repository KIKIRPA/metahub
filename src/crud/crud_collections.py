from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId

import core
from crud.base import CRUDBase, NoResultsError, DependentObjectsError, translate_from_mongo


class CRUDCollection(CRUDBase):
    async def get_by_keys(
            self, 
            collection: AsyncIOMotorCollection, 
            *,
            collection_name: str) -> dict:
        result = await collection.find_one({
            "collection_name": collection_name})
        if result is None: raise NoResultsError
        return translate_from_mongo(result)


    async def cascading_replace(
            self,
            collection: AsyncIOMotorCollection,
            id: str,
            *,
            data: dict) -> dict:
        # get the existing collection
        original_data = await collection.find_one({"_id": ObjectId(id)})
        if original_data is None: raise NoResultsError

        # replace collection
        result = await self.replace(
            collection=collection, 
            id=id,
            data=data,
            original_data=original_data)

        # update related samples
        if data["collection_name"] != original_data["collection_name"]:
            client = AsyncIOMotorClient(core.settings.mongo_conn_str)
            db = client[core.settings.mongo_db]
            await db.samples.update_many(
                {"collection.collection_id": id},
                {
                    "$set": {
                        "collection.collection_name": result["collection_name"],
                        "modified_timestamp": datetime.now(timezone.utc)
                    }
                })

        return result


    async def safe_remove(
            self,
            collection: AsyncIOMotorCollection,
            *,
            id: str)-> dict:
        # check if there are samples in this collection
        client = AsyncIOMotorClient(core.settings.mongo_conn_str)
        db = client[core.settings.mongo_db]
        number_of_samples = db.samples.count_documents(
            {"collection.collection_id": id},
            limit=1)
        
        # remove project (if it contains no samples)
        if number_of_samples == 0:
            result = await self.remove(
                collection=collection, 
                id=id)
            return translate_from_mongo(result)
        else:
            raise DependentObjectsError


collection = CRUDCollection()