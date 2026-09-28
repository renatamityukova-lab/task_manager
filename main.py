import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException

# добавляем корень проекта в sys.path, чтобы работал абсолютный импорт
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from task_manager.models import TaskCreate, TaskResponse

app = FastAPI(
    title="Task Manager API",
    description="REST API для управления задачами",
    version="1.0.0",
)

tasks: list[dict] = []
next_id: int = 1


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=201,
    description="Создать новую задачу",
)
def create_task(payload: TaskCreate) -> TaskResponse:
    global next_id

    task = {
        "id": next_id,
        "title": payload.title,
        "description": payload.description,
        "priority": payload.priority,
    }
    next_id += 1
    tasks.append(task)

    return task


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=200,
    description="Получить задачу по ID",
)
def get_task(task_id: int) -> TaskResponse:
    for task in tasks:
        if task["id"] == task_id:
            return task

    raise HTTPException(status_code=404, detail={"detail": "Task not found", "task_id": task_id})
