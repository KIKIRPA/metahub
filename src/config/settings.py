from functools import lru_cache

from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Meta"
    admin_email: str = "hescida@kikirpa.be"
    mongo_conn_str: str = "mongodb://kikirpa:hescida@localhost:27017/"
    mongo_db: str = "meta"
    documents_collection: str = "documents"
    activities_collection: str = "activities"
    templates_collection: str = "templates"
    json_schema_version: str = "http://json-schema.org/draft-07/schema#"

    class Config:
        env_file = ".env"


# Get config settings
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()