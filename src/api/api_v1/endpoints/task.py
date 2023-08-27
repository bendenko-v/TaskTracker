from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud.crud_task import task as crud
from src.crud.crud_employee import employee as crud_emp
from src.database import get_db
from src.schemas import TaskCreateScheme, TaskScheme, TaskImportantScheme
from src.services import get_important_tasks_service

router = APIRouter()


@router.get('/important', response_model=list[TaskImportantScheme])
def get_important_tasks(db: Session = Depends(get_db)):
    """ Get important tasks """
    if tasks := get_important_tasks_service(crud.get_important_tasks(db), crud_emp.less_busy_employee(db)):
        return tasks
    else:
        raise HTTPException(status_code=404, detail='No important tasks found')


@router.get('', response_model=list[TaskScheme])
def get_tasks(db: Session = Depends(get_db)):
    """Get all tasks"""
    tasks = crud.get_all(db)
    if not tasks:
        raise HTTPException(status_code=404, detail='Tasks not found')
    return tasks


@router.get('/{task_id}', response_model=TaskScheme)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get task by id"""
    task = crud.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f'Task with id {task_id} not found')
    return task


@router.post('')
def create_task(task: TaskCreateScheme, db: Session = Depends(get_db)):
    """Create task"""
    return crud.create(db, task)


@router.put('/{task_id}')
def update_task(task_id: int, data: TaskCreateScheme, db: Session = Depends(get_db)):
    """Update task"""
    return crud.update(db, task_id, data)
