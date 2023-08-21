from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db
from .schemas import TaskScheme, TaskCreateScheme
from . import crud

tasks_router = APIRouter(prefix='/tasks', tags=['tasks'])


@tasks_router.get('', response_model=list[TaskScheme])
def get_tasks(db: Session = Depends(get_db)):
    """ Get all tasks """
    tasks = crud.get_all_tasks(db)
    if not tasks:
        return JSONResponse(content={'message': 'No tasks found'}, status_code=404)
    return tasks


@tasks_router.get('/{task_id}', response_model=TaskScheme)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """ Get task by id """
    task = crud.get_task_by_id(db, task_id)
    if not task:
        return JSONResponse(content={'message': f'No task with id {task_id} found'}, status_code=404)
    return task


@tasks_router.post('')
def create_task(task: TaskCreateScheme, db: Session = Depends(get_db)):
    """ Create task """
    return crud.create_task(db, task)


@tasks_router.put('/{task_id}')
def update_task(task_id: int, data: TaskCreateScheme, db: Session = Depends(get_db)):
    """ Update task """
    return crud.update_task(db, task_id, data)
