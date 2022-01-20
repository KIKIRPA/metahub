from functools import lru_cache

from pydantic import BaseSettings

from core.enums import JsonSchemaVersion

class Settings(BaseSettings):
    app_name: str = "Meta"
    admin_email: str = "hescida@kikirpa.be"
    mongo_conn_str: str = "mongodb://kikirpa:hescida@localhost:27017/"
    mongo_db: str = "meta"
    documents_collection: str = "documents"
    projects_collection: str = "projects"
    templates_collection: str = "templates"
    json_schema_version: JsonSchemaVersion = JsonSchemaVersion.DRAFT7
    json_schema_base_url: str = "https://balat.kikirpa.be/schema"

    class Config:
        env_file = ".env"


# Get config settings
@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()