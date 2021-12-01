from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Meta"
    admin_email: str = "hescida@kikirpa.be"
    mongo_conn_str: str = "mongodb://kikirpa:hescida@localhost:27017/"
    mongo_db: str = "meta"
    documents_collection: str = "documents"
    templates_collection: str = "templates"

    class Config:
        env_file = ".env"