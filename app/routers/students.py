from typing import Any

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

from app.models import Student, StudentCreate

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Student)
async def create_student(*, student: StudentCreate) -> Any:
    student_data = student.model_dump()
    db_student = Student.model_validate(student_data)
    await db_student.insert()
    return db_student


@router.get("/")
async def read_students() -> list[Student]:
    students = await Student.find().to_list(1000)
    return students


@router.get("/{student_id}", response_model=Student)
async def read_student(*, student_id: PydanticObjectId) -> Any:
    student = await Student.get(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student {student_id!r} not found",
        )
    return student


# @router.patch("/{student_id}", response_model=Student)
# async def update_student(
#     *, student_id: PydanticObjectId, student: UpdateStudent
# ) -> Any:
#     student_data = student.model_dump(exclude_unset=True)
#     db_student = await Student.get(student_id)
#     if not db_student:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Student {student_id!r} not found",
#         )
#     await db_student.update(student_data)
#     # db_student = await Student.find_one_and_update(
#     #     {"_id": ObjectId(student_id)},
#     #     {"$set": student_data},
#     #     return_document=ReturnDocument.AFTER,
#     # )
#     return db_student


# @router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_student(*, student_id: str) -> None:
#     result = await student_collection.delete_one({"_id": ObjectId(student_id)})
#     if not result.deleted_count:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Student {student_id!r} not found",
#         )
