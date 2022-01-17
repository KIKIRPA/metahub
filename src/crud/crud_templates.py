from motor.motor_asyncio import AsyncIOMotorCollection

from crud.base import CRUDBase, NoResultsError, translate_id
import models


class CRUDTemplate(CRUDBase):
    async def get_by_keys(
            self, 
            collection: AsyncIOMotorCollection, 
            *,
            resource: models.Resource,
            category: str,
            template: str = "_default") -> dict:
        result = await collection.find_one({
            "resource": resource.value, 
            "category": category, 
            "template": template})
        if result is None: raise NoResultsError
        return translate_id(result)


template = CRUDTemplate()