from fastapi import APIRouter, HTTPException, Path

from models.document_types import document_types

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/schemas",
    tags=["schemas"]
)


@router.get("/{document_type}")
async def read_measurement_schema(document_type: str = Path(None, description="The type of report or measurement")):
    """Displaying json-schema.
    """

    if document_type not in document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")

    return document_types[document_type]["model"].schema()

