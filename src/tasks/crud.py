from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session

from .models import TasksModel
from .schemas import TaskCreateScheme


def get_all_tasks(db: Session) -> list[TasksModel]:
    return db.query(TasksModel).all()


def get_task_by_id(db: Session, task_id: int) -> TasksModel:
    return db.query(TasksModel).filter(TasksModel.id == task_id).first()


def create_task(db: Session, data: TaskCreateScheme) -> JSONResponse:
    try:
        task = TasksModel(**data.model_dump())
        db.add(task)
        db.commit()
    except ValidationError as err:
        raise HTTPException(status_code=400, detail=err.messages)
    return JSONResponse(content={'message': 'Task created'}, status_code=status.HTTP_201_CREATED)


def update_task(db: Session, task_id: int, data: TaskCreateScheme) -> JSONResponse:
    try:
        db.query(TasksModel).filter(TasksModel.id == task_id).update(data.model_dump())
        db.commit()
    except ValidationError as err:
        raise HTTPException(status_code=400, detail=err.messages)
    return JSONResponse(content={'message': 'Task data updated'}, status_code=status.HTTP_204_NO_CONTENT)


