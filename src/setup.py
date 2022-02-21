from datetime import datetime, timezone
from glob import glob
import os
from optparse import OptionParser
import json

import asyncio
import pymongo
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi.encoders import jsonable_encoder

import core
import models


async def drop(db: AsyncIOMotorDatabase, collection: str):
    existing_collections = await db.list_collection_names()
    if collection in existing_collections:
        await db.drop_collection(collection)
        print(f" - Dropped collection '{collection}'")


async def seed(db: AsyncIOMotorDatabase, collection: str, list_of_files: list, model=None):
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
            if model is not None:
                item = model.parse_file(file)
                # first encode for json
                item = item.dict()
            else:
                with open(file) as json_file:
                    item = json.load(json_file)
            item = jsonable_encoder(item)
            item["created_timestamp"] = datetime.now(timezone.utc)
            item["modified_timestamp"] = item["created_timestamp"]
            inserted = await db[collection].insert_one(item)
            item = await db[collection].find_one({"_id": inserted.inserted_id})
            print(f" - Seeded file: {os.path.basename(file)}")
        except:
            print(f" ! Seed failed on: {os.path.basename(file)}")


async def main():
    # OPTIONPARSER
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-d", "--drop", help="Drop existing collections", action="store_true", dest="drop", default=False) 
    parser.add_option("-T", "--seed-templates", action="append", dest="seed_templates", help="Seed templates")
    parser.add_option("-P", "--seed-projects", action="append", dest="seed_projects", help="Seed projects")
    parser.add_option("-D", "--seed-datasets", action="append", dest="seed_datasets", help="Seed datasets")
    parser.add_option("-C", "--seed-collections", action="append", dest="seed_collections", help="Seed collections")
    parser.add_option("-S", "--seed-samples", action="append", dest="seed_samples", help="Seed samples")
    (options, args) = parser.parse_args()
    
    # MONGO CONNECTION
    client = AsyncIOMotorClient(core.settings.mongo_conn_str)
    db = client[core.settings.mongo_db]


    mongo_collections = [
        {
            "name": "templates",
            "unique_index": [
                ('resource', pymongo.ASCENDING),
                ('category', pymongo.ASCENDING),
                ('template', pymongo.ASCENDING)
            ],
            "seed_templates": options.seed_templates,
            "model": models.TemplateUpdate
        },
        {
            "name": "projects",
            "unique_index": [
                ('project_code', pymongo.ASCENDING),
                ('unit', pymongo.ASCENDING)
            ],
            "seed_templates": options.seed_projects,
            "model": None
        },
        {
            "name": "datasets",
            "unique_index": [
                ('dataset_code', pymongo.ASCENDING)
            ],
            "seed_templates": options.seed_datasets,
            "model": None
        },
        {
            "name": "collections",
            "unique_index": [
                ('collection_code', pymongo.ASCENDING)
            ],
            "seed_templates": options.seed_collections,
            "model": None
        },
        {
            "name": "samples",
            "unique_index": [
                ('sample_code', pymongo.ASCENDING),
                ('collection_id', pymongo.ASCENDING),
            ],
            "seed_templates": options.seed_samples,
            "model": None
        }
    ]

    for collection in mongo_collections:
        print(f"\n{collection['name'].upper()} COLLECTION")

        if options.drop:
            await drop(db, collection['name'])

        try:
            await db[collection['name']].create_index(collection['unique_index'], unique=True)
            print(f" - Created collection '{collection['name']}' and an index with a unique restraint")
        except:
            print(f" ! Error in creating collection '{collection['name']}' and an index with a unique restraint")

        if options.seed_templates is not None:
            await seed(db, collection['name'], collection['seed_templates'], collection['model'])

    print("\n")


if __name__ == '__main__' and __package__ is None:
    loop = asyncio.run(main())