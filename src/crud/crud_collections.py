from motor.motor_asyncio import AsyncIOMotorCollection

from crud.base import CRUDBase, NoResultsError, translate_from_mongo


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


collection = CRUDCollection()