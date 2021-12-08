import sys, importlib
from pathlib import Path
from glob import glob
import os

from functools import lru_cache

from optparse import OptionParser

import asyncio
import motor.motor_asyncio


def import_parents(level=1):
    global __package__
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[level]
    
    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError: # already removed
        pass

    __package__ = '.'.join(parent.parts[len(top.parts):])
    importlib.import_module(__package__) # won't be needed after that


@lru_cache()
def get_settings():
    return Settings()


async def main():   
    # READ CONFIG
    config = get_settings()

    # MONGO CONNECTION
    client = motor.motor_asyncio.AsyncIOMotorClient(config.mongo_conn_str)
    db = client[config.mongo_db]

    await db.drop_collection(config.activities_collection)
    print("Dropped collection '" + config.templates_collection + "'\n")

    collections = await db.list_collection_names()
    print("\nCollections: " + str(collections) + "\n")

    

    print('\n')

if __name__ == '__main__' and __package__ is None:
    import_parents(level=2)
    from ..config import Settings

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())