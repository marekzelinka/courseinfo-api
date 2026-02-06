from typing import Annotated

from bson import ObjectId
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
    UrlConstraints,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    mongodb_uri: Annotated[
        MultiHostUrl,
        UrlConstraints(allowed_schemes=["mongodb", "mongodb+srv"]),
    ]


class Student(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": 3.0,
            }
        },
    )

    id: PyObjectId | None = Field(default=None, alias="_id")
    name: str
    email: EmailStr
    course: str
    gpa: float = Field(le=4.0)


class UpdateStudent(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": 3.0,
            }
        },
    )

    name: str | None = None
    email: EmailStr | None = None
    course: str | None = None
    gpa: float | None = None
