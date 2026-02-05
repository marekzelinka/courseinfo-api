from bson import ObjectId
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.db import PyObjectId


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
