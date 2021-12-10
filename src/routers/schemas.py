from mergedeep import merge

from fastapi import APIRouter, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient

import config

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/schema",
    tags=["schema"]
)


@router.get("/document/{document_type}")
async def read_measurement_schema(
        document_type: str = Path(None, description="The type of report or measurement")):
    """
    Displaying json-schema.
    """

    if document_type not in config.document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")

    return config.document_types[document_type]["model"].schema()


@router.get("/document/{document_type}/{template}")
async def read_measurement_schema(
        document_type: str = Path(None, description="The type of report or measurement"),
        template: str = Path(None, description="Schema template to be applied")):
    """
    Displaying json-schema with an applied schema template.
    """

    if document_type not in config.document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")
    schema = config.document_types[document_type]["model"].schema()

    client = AsyncIOMotorClient(config.settings.mongo_conn_str)
    db = client[config.settings.mongo_db]

    if (response := await db[config.settings.templates_collection].find_one({"alias": template, "schemas": document_type})) is None:
        raise HTTPException(status_code=404, detail="Template type does not exist (for the given document type)")

    return merge({}, schema, response["template"])
