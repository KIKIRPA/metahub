from motor.motor_asyncio import AsyncIOMotorCollection

from crud.base import CRUDBase, NoResultsError, translate_from_mongo


class CRUDDataset(CRUDBase):
    async def get_by_keys(
            self, 
            collection: AsyncIOMotorCollection, 
            *,
            dataset_code: str) -> dict:
        result = await collection.find_one({
            "dataset_code": dataset_code})
        if result is None: raise NoResultsError
        return translate_from_mongo(result)


dataset = CRUDDataset()