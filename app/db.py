from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

from app.models import Settings

config = Settings()

client = AsyncMongoClient(
    str(config.mongodb_uri),
    server_api=ServerApi(version="1", strict=True, deprecation_errors=True),
)
db = client.get_database("college")

student_collection = db.get_collection("students")
