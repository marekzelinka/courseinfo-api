from typing import Annotated

from pydantic import BeforeValidator
from pymongo import AsyncMongoClient
from pymongo.server_api import ServerApi

from app.core.config import config

client = AsyncMongoClient(
    str(config.mongodb_uri),
    server_api=ServerApi(version="1", strict=True, deprecation_errors=True),
)
db = client.get_database("college")

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

student_collection = db.get_collection("students")
