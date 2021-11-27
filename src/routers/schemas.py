from fastapi import APIRouter, HTTPException, Path

from models.document_types import document_types, test_document_templates

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/schemas",
    tags=["schemas"]
)


def merge(source, destination):
    """
    Recursively merge two dicts
    """
    for key, value in destination.items():
        if isinstance(value, dict):
            # get node or create one
            node = source.setdefault(key, {})
            merge(value, node)
        else:
            source[key] = value

    return source


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
        template: str = Path(None, description="Schema template to be applied")):
    """
    Displaying json-schema with an applied schema template.
    """

    if document_type not in document_types:
        raise HTTPException(status_code=404, detail="Document type does not exist")

    if template not in test_document_templates:
        raise HTTPException(status_code=404, detail="Template type does not exist (for the given document type)")

    schema = merge(document_types[document_type]["model"].schema(), test_document_templates[template]["template"])

    return schema