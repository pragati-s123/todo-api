from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, field_validator

app = FastAPI(
    title="To-Do List API",
    description="A simple CRUD API for managing tasks in memory.",
    version="1.0.0",
)


# In-memory storage
tasks = []
next_id = 1


# Request/Response Models
class TaskCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip()


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Title cannot be empty")
        return value.strip() if value is not None else value


class Task(BaseModel):
    id: int
    title: str
    done: bool


# Helper function
def get_task_by_id(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


# Create a new task
@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    global next_id

    task = {
        "id": next_id,
        "title": task_data.title,
        "done": False,
    }

    tasks.append(task)
    next_id += 1

    return task


# List all tasks
@app.get("/tasks", response_model=list[Task], status_code=status.HTTP_200_OK)
def list_tasks():
    return tasks


# Get a single task by ID
@app.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: int):
    task = get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Task with id {task_id} not found"},
        )

    return task


# Update a task
@app.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task_update: TaskUpdate):
    task = get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Task with id {task_id} not found"},
        )

    if task_update.title is not None:
        task["title"] = task_update.title

    if task_update.done is not None:
        task["done"] = task_update.done

    return task


# Delete a task
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    task = get_task_by_id(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": f"Task with id {task_id} not found"},
        )

    tasks.remove(task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Convert validation errors for empty title into HTTP 400
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return Response(
        content='{"message":"Title cannot be empty"}',
        status_code=status.HTTP_400_BAD_REQUEST,
        media_type="application/json",
    )


# Run with:
# uvicorn main:app --reload
#
# Swagger UI:
# http://127.0.0.1:8000/docs
#
# ReDoc:
# http://127.0.0.1:8000/redoc