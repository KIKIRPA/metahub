from functools import lru_cache
from typing import Literal

from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Meta"
    admin_email: str = "hescida@kikirpa.be"

    mongo_conn_str: str = "mongodb://kikirpa:hescida@localhost:27017/"
    mongo_db: str = "meta"

    resource_name_project: str = "project"
    resource_name_dataset: str = "dataset"
    resource_name_collection: str = "collection"
    resource_name_sample: str = "sample"
    
    json_schema_version: Literal[
        'DRAFT202012', 
        'DRAFT201909', 
        'DRAFT7',
        'DRAFT6',
        'DRAFT4',
        'DRAFT3'] = "DRAFT7"
    json_schema_base_url: str = "https://balat.kikirpa.be/schema"

    class Config:
        env_file = ".env"


# Get config settings
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()