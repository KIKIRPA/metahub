from fastapi import APIRouter, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient

import core
import core.utils.files
import crud



# Creating a FastAPI router, meaning a set of routes that can be included later
# in the FastAPI application
router = APIRouter(
    prefix="/api/v1/files",
    tags=["api/v1/files"])

# Creating a MongoDB client and connect to the relevant collections
client = AsyncIOMotorClient(core.settings.mongo_conn_str)
db = client[core.settings.mongo_db]


#
#   FILES ROUTES
#

@router.get("/project_path/{project_id}")
async def get_files_in_project_path(
        project_id: str = Path(None, description="The id of the project")):
    """
    Return the files and directories in the project path.
    """
    # get project from db
    try:
        project = await crud.project.get(
            collection=db.projects, 
            id=project_id)
    except crud.NoResultsError:
        raise HTTPException(status_code=404, detail="NoResults")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))

    # check if this project has a path
    if "path" not in project or project["path"] is None:
        raise HTTPException(status_code=404, detail="NoProjectPath")
    
    # read and return directory structure of this path
    try:
        response = core.utils.files.read_path(project["path"])
    except core.utils.files.DirectoryNotFoundError:
        raise HTTPException(status_code=404, detail="DirectoryNotFound")
    except core.utils.files.DirectoryNotReadableError:
        raise HTTPException(status_code=404, detail="DirectoryNotReadableError")
    except BaseException as err:
        raise HTTPException(status_code=400, detail=str(err))
    return response