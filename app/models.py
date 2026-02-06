from beanie import Document
from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    name: str
    email: EmailStr
    course: str
    gpa: float = Field(le=4.0)


class Student(Document, StudentBase):
    pass


class StudentCreate(StudentBase):
    pass


class UpdateStudent(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    course: str | None = None
    gpa: float | None = None
