from fastapi import APIRouter

from models.measurement import Measurement
from models.drms import DRMS

# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/schemas",
    tags=["schemas"]
)


@router.get("/measurement")
async def read_measurement_schema():
    """Displaying json-schema.
    """
    return Measurement.schema()

