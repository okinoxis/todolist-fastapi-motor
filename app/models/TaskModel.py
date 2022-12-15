from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId
from app.db import PyObjectId

class TaskBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    text: Optional[str]
    completed: Optional[bool]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "_id": "63894321e0649e03135b4d86",
                "text": "This is a new task to be completed",
                "completed": "false",
                "created_at": "2022-12-01T21:13:10.602268",
                "updated_at": "2022-12-01T21:13:10.602277"
            }
        }

class TaskCreateModel(TaskBaseModel):
    text: str
    completed: bool = False
    created_at: str = str(datetime.now())
    updated_at: str = str(datetime.now())

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "text": "This is a new task to be completed",
            }
        }


class TaskUpdateModel(TaskBaseModel):
    text: Optional[str]
    completed: Optional[bool]
    updated_at: str = str(datetime.now())
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "text": "This is a edited task to be completed",
                "completed": "true"
            }
        }