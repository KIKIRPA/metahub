from functools import lru_cache
from mergedeep import merge

from fastapi import APIRouter, HTTPException, Path, Depends
import motor.motor_asyncio

from config import Settings
from models.document_types import document_types

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/schemas",
    tags=["schemas"]
)

@lru_cache()
def get_settings():
    return Settings()


@router.get("/{document_type}")
async def read_measurement_schema(
        document_type: str = Path(None, description="The type of report or measurement")):
    """
    Displaying json-schema.
    """

    if document_type not in document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")

    return document_types[document_type]["model"].schema()


@router.get("/{document_type}/{template}")
async def read_measurement_schema(
        document_type: str = Path(None, description="The type of report or measurement"),
        template: str = Path(None, description="Schema template to be applied"),
        config: Settings = Depends(get_settings)):
    """
    Displaying json-schema with an applied schema template.
    """

    if document_type not in document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")
    schema = document_types[document_type]["model"].schema()

    client = motor.motor_asyncio.AsyncIOMotorClient(config.mongo_conn_str)
    db = client[config.mongo_db]

    if (response := await db[config.templates_collection].find_one({"alias": template, "schemas": document_type})) is None:
        raise HTTPException(status_code=404, detail="Template type does not exist (for the given document type)")

    return merge({}, schema, response["template"])
