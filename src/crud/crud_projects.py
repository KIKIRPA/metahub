from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from bson import ObjectId

import core
from crud.base import CRUDBase, NoResultsError, translate_from_mongo
from models.common import Unit


class CRUDProject(CRUDBase):
    async def get_by_keys(
            self, 
            collection: AsyncIOMotorCollection, 
            *,
            project_code: str,
            unit: Unit) -> dict:
        result = await collection.find_one({
            "project_code": project_code, 
            "unit": unit.value})
        if result is None: raise NoResultsError
        return translate_from_mongo(result)


    async def cascading_replace(
            self,
            collection: AsyncIOMotorCollection,
            id: str,
            *,
            data: dict) -> dict:
        # get the existing project
        original_data = await collection.find_one({"_id": ObjectId(id)})
        if original_data is None: raise NoResultsError

        # replace project
        result = await self.replace(
            collection=collection, 
            id=id,
            data=data,
            original_data=original_data)

        # update related datasets
        if data["project_code"] != original_data["project_code"] or data["unit"] != original_data["unit"]:
            print("UPDATE MANY")
            client = AsyncIOMotorClient(core.settings.mongo_conn_str)
            db = client[core.settings.mongo_db]
            await db.datasets.update_many(
                {"project.project_id": id,},
                {
                    "$set": {
                        "project.project_code": result["project_code"],
                        "project.unit": result["unit"],
                        "modified_timestamp": datetime.now(timezone.utc)
                    }
                })

        return result


project = CRUDProject()