from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId

import core
from crud.base import CRUDBase, NoResultsError, translate_from_mongo


class CRUDSample(CRUDBase):
    async def get_by_keys(
            self, 
            collection: AsyncIOMotorCollection, 
            *,
            sample_code: str,
            collection_id: str) -> dict:
        result = await collection.find_one({
            "sample_code": sample_code,
            "collection.collection_id": collection_id})
        if result is None: raise NoResultsError
        return translate_from_mongo(result)


    async def cascading_replace(
            self,
            collection: AsyncIOMotorCollection,
            id: str,
            *,
            data: dict) -> dict:
        # get the existing sample
        original_data = await collection.find_one({"_id": ObjectId(id)})
        if original_data is None: raise NoResultsError

        # replace sample
        result = await self.replace(
            collection=collection, 
            id=id,
            data=data,
            original_data=original_data)

        # update parent_sample in child samples
        if data["sample_code"] != original_data["sample_code"]:
            client = AsyncIOMotorClient(core.settings.mongo_conn_str)
            db = client[core.settings.mongo_db]
            await db.samples.update_many(
                {"parent_sample.parent_sample_id": id},
                {
                    "$set": {
                        "parent_sample.parent_sample_code": result["sample_code"],
                        "modified_timestamp": datetime.now(timezone.utc)
                    }
                })

        return result


    async def cascading_remove(
            self,
            collection: AsyncIOMotorCollection,
            *,
            id: str)-> dict:
        # remove sample
        result = await self.remove(
            collection=collection, 
            id=id)
        # update parent_sample in child samples
        client = AsyncIOMotorClient(core.settings.mongo_conn_str)
        db = client[core.settings.mongo_db]
        await db.samples.update_many(
            {"parent_sample.parent_sample_id": id},
            {
                "$unset": {
                    "parent_sample": "",
                },
                "$set": {
                    "modified_timestamp": datetime.now(timezone.utc)
                }
            })
        return result


sample = CRUDSample()