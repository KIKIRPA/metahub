from motor.motor_asyncio import AsyncIOMotorCollection

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
            "collection.collection.id": collection_id})
        if result is None: raise NoResultsError
        return translate_from_mongo(result)


sample = CRUDSample()