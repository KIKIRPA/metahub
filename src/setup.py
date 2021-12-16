import sys, importlib
from pathlib import Path
from glob import glob
import os
from optparse import OptionParser

import asyncio
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi.encoders import jsonable_encoder

import config
import models
from models.document_templates import DocumentTemplate


async def drop(db: AsyncIOMotorDatabase, collection: str):
    existing_collections = await db.list_collection_names()
    if collection in existing_collections:
        await db.drop_collection(collection)
        print(f" - Dropped collection '{collection}'")


async def seed(db: AsyncIOMotorDatabase, collection: str, list_of_files: list, model):
    files = []
    for item in list_of_files:
        files.extend(glob(item))
    files = list(set(files)) #remove duplicates
    for file in files:
        if os.path.isdir(file):
            files.remove(file)   #remove directories
    if len(files) == 0:
        print(f" ! No data to seed for collection '{collection}'")
        return

    for file in files:
        try: 
            item = model.parse_file(file)
            item = jsonable_encoder(item)
            inserted = await db[collection].insert_one(item)
            item = await db[collection].find_one({"_id": inserted.inserted_id})
            print(f" - Seeded file: {os.path.basename(file)}")
        except:
            print(f" ! Seed failed on: {os.path.basename(file)}")


async def main():
    # OPTIONPARSER
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-d", "--drop", help="Drop existing collections", action="store_true", dest="drop", default=False) 
    parser.add_option("-T", "--seed-templates", action="append", dest="seed_templates", help="Seed template files")
    (options, args) = parser.parse_args()
    
    # MONGO CONNECTION
    client = AsyncIOMotorClient(config.settings.mongo_conn_str)
    db = client[config.settings.mongo_db]

    # TEMPLATE COLLECTION
    print("\nTEMPLATE COLLECTION")
    collection = config.settings.templates_collection
    if options.drop:
        await drop(db, collection)

    try:
        await db[collection].create_index([
            ('category', pymongo.ASCENDING),
            ('schema_id', pymongo.ASCENDING),
            ('template_id', pymongo.ASCENDING)], unique=True)
        print(f" - Created collection '{collection}' and an index with a unique restraint")
    except:
        print(f" ! Error in creating collection '{collection}' and an index with a unique restraint")

    if len(options.seed_templates) > 0:
        await seed(db, collection, options.seed_templates, models.Template)

    print("\n")

if __name__ == '__main__' and __package__ is None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())