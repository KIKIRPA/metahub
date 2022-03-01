from motor.motor_asyncio import AsyncIOMotorCollection

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


project = CRUDProject()