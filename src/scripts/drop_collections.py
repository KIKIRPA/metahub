import sys, importlib
from pathlib import Path

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


async def main():   
    # MONGO CONNECTION
    client = motor.motor_asyncio.AsyncIOMotorClient(config.settings.mongo_conn_str)
    db = client[config.settings.mongo_db]

    await db.drop_collection(config.settings.activities_collection)
    print("Dropped collection '" + config.settings.templates_collection + "'\n")

    collections = await db.list_collection_names()
    print("\nCollections: " + str(collections) + "\n")

if __name__ == '__main__' and __package__ is None:
    import_parents(level=2)
    from .. import config

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())