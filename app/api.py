from typing import Any

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from pymongo import ReturnDocument

from app.db import student_collection
from app.models import Student, UpdateStudent

router = APIRouter()


@router.post(
    "/students",
    status_code=status.HTTP_201_CREATED,
    response_model=Student,
    response_model_by_alias=False,
)
async def create_student(*, student: Student) -> Any:
    db_student = student.model_dump(by_alias=True, exclude={"id"})
    result = await student_collection.insert_one(db_student)
    db_student["_id"] = result.inserted_id
    return db_student


@router.get("/students", response_model=list[Student], response_model_by_alias=False)
async def read_students() -> Any:
    students = await student_collection.find().to_list(1000)
    return students


@router.get(
    "/students/{student_id}", response_model=Student, response_model_by_alias=False
)
async def read_student(*, student_id: str) -> Any:
    student = await student_collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student {student_id!r} not found",
        )
    return student


@router.patch(
    "/students/{student_id}", response_model=Student, response_model_by_alias=False
)
async def update_student(*, student_id: str, student: UpdateStudent) -> Any:
    student_data = student.model_dump(by_alias=True, exclude_unset=True)
    db_student = await student_collection.find_one_and_update(
        {"_id": ObjectId(student_id)},
        {"$set": student_data},
        return_document=ReturnDocument.AFTER,
    )
    if not db_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student {student_id!r} not found",
        )
    return db_student


@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(*, student_id: str) -> None:
    result = await student_collection.delete_one({"_id": ObjectId(student_id)})
    if not result.deleted_count:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student {student_id!r} not found",
        )
