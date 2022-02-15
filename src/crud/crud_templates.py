from motor.motor_asyncio import AsyncIOMotorCollection

from core.enums import Resource
from crud.base import CRUDBase, NoResultsError, translate_from_mongo
import models


class CRUDTemplate(CRUDBase):
    async def get_by_keys(
            self, 
            collection: AsyncIOMotorCollection, 
            *,
            resource: Resource,
            category: str,
            template: str = "_default") -> dict:
        result = await collection.find_one({
            "resource": resource.value, 
            "category": category, 
            "template": template})
        if result is None: raise NoResultsError
        return translate_from_mongo(result)


template = CRUDTemplate()