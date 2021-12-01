import sys, importlib
from pathlib import Path
from glob import glob
import os

from functools import lru_cache

from optparse import OptionParser

import asyncio
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder


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
    # OPTIONPARSER
    parser = OptionParser(usage="usage: %prog [options] JSON_FILES")
    parser.add_option("-d", "--drop", help="Drop existing collection", action="store_true", dest="drop", default=False) 
    (options, args) = parser.parse_args()
    
    # READ CONFIG
    config = get_settings()

    # MONGO CONNECTION
    client = motor.motor_asyncio.AsyncIOMotorClient(config.mongo_conn_str)
    db = client[config.mongo_db]

    collections = await db.list_collection_names()
    print("\nCollections: " + str(collections) + "\n")

    # DROP COLLECTION
    if options.drop:
        if config.templates_collection in collections:
            await db.drop_collection(config.templates_collection)
            print("Dropped collection '" + config.templates_collection + "'\n")
        else:
            print("Collection '" + config.templates_collection + "' does not exist and cannot be deleted\n")

    # LIST JSONS FOR SEEDING
    jsons = []
    if len(args) == 0:
        print("No json files?\n")
        exit()
    else:
        for arg in args:
            jsons.extend(glob(arg))
    jsons = list(set(jsons)) #remove duplicates
    for json in jsons:
        if os.path.isdir(json):
            jsons.remove(json)   #remove directories
    if len(jsons) == 0:
        print("No json files?\n")
        exit()

    # READ JSON FILES AND SEED
    print("Seeding:")
    for json in jsons:
        #with open(json,'r') as fh:
        #    json_str = fh.read()
        template = DocumentTemplate.parse_file(json)
        template = jsonable_encoder(template)
        inserted = await db[config.templates_collection].insert_one(template)
        template = await db[config.templates_collection].find_one({"_id": inserted.inserted_id})
        print(" - " + template["title"])

    print('\n')

if __name__ == '__main__' and __package__ is None:
    import_parents(level=2)
    from ..config import Settings
    from ..models.document_template import DocumentTemplate

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())