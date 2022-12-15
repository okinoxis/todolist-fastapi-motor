from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.db import db
from app.models.TaskModel import TaskBaseModel, TaskCreateModel, TaskUpdateModel
from typing import List


router = APIRouter()


@router.get(
    "/", response_description="List all tasks", response_model=List[TaskBaseModel]
)
async def get_all_tasks():
    cursor = db["tasks"].find().sort("_id", -1)
    tasks = await cursor.to_list(1000)
    return tasks


@router.get(
    "/{id}", response_description="Get a single task", response_model=TaskBaseModel
)
async def get_one_task(id: str):
    if (task := await db["tasks"].find_one({"_id": id})) is not None:
        return task
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content=f"Task {id} not found"
    )


@router.post(
    "/create", response_description="Add new task", response_model=TaskBaseModel
)
async def create_task(task: TaskCreateModel = Body(...)):
    task = jsonable_encoder(task)
    new_task = await db["tasks"].insert_one(task)
    created_task = await db["tasks"].find_one({"_id": new_task.inserted_id})
    await db["tasks"].create_index("_id")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_task)


@router.put(
    "/update/{id}", response_description="Update task", response_model=TaskBaseModel
)
async def update_task(id: str, task: TaskUpdateModel = Body(...)):
    update_task = dict(task)
    new_document = await db["tasks"].update_one(
        {"_id": id},
        {"$set": {"text": update_task["text"], "completed": update_task["completed"]}},
    )
    if (new_document := await db["tasks"].find_one({"_id": id})) is not None:
        return JSONResponse(status_code=status.HTTP_200_OK, content=new_document)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content=f"Task {id} not found"
    )


@router.delete("/delete/{id}", response_description="Delete task")
async def delete_task(id: str):
    result = await db["tasks"].delete_one({"_id": id})
    if (result) is not None:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=f"Task {id} removed successfully"
        )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content=f"Task {id} not found"
    )
