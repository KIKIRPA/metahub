from functools import lru_cache
from enum import Enum

from pydantic import BaseSettings


class JsonSchemaVersion(str, Enum):
    DRAFT3 = 'http://json-schema.org/draft-03/schema#'
    DRAFT4 = 'http://json-schema.org/draft-04/schema#'
    DRAFT6 = 'http://json-schema.org/draft-06/schema#'
    DRAFT7 = 'http://json-schema.org/draft-07/schema#'
    DRAFT201909 = 'https://json-schema.org/draft/2019-09/schema'
    DRAFT202012 = 'https://json-schema.org/draft/2020-12/schema'


class Settings(BaseSettings):
    app_name: str = "Meta"
    admin_email: str = "hescida@kikirpa.be"
    mongo_conn_str: str = "mongodb://kikirpa:hescida@localhost:27017/"
    mongo_db: str = "meta"
    documents_collection: str = "documents"
    activities_collection: str = "activities"
    templates_collection: str = "templates"
    json_schema_version: JsonSchemaVersion = JsonSchemaVersion.DRAFT7

    class Config:
        env_file = ".env"


# Get config settings
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()