from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy import func, exists
from sqlalchemy.orm import Session, joinedload

from .models import TasksModel, StatusEnum
from .schemas import TaskCreateScheme, TaskScheme, TaskImportantScheme
from ..employee.models import EmployeeModel


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


def get_important_tasks(db: Session) -> list[TaskImportantScheme]:
    # Get important tasks (where task has parent and no employee assigned) """
    important_tasks = (
        db.query(TasksModel)
        .filter(TasksModel.employee_id == None, TasksModel.parent_id != None)
    ).all()

    if not important_tasks:
        raise HTTPException(status_code=404, detail='Tasks not found')

    # Get employees with active tasks in ascending order """
    employees = (
        db.query(EmployeeModel, func.count(TasksModel.id).label('task_count'))
        .outerjoin(TasksModel, EmployeeModel.id == TasksModel.employee_id)
        .group_by(EmployeeModel.id)
        .order_by(func.count(TasksModel.id).asc())
    ).all()

    if not employees:
        raise HTTPException(status_code=404, detail='Employees not found')

    # Processing of received data
    tasks_data = {t.parent_id: t.id for t in important_tasks}
    print(tasks_data)
    emp_data = {
        emp.id: {
            'employee': emp,
            'tasks': [t.id for t in emp.tasks if t.status == StatusEnum.doing],
            'active_tasks': active_tasks,
        }
        for emp, active_tasks in employees
    }

    employments_list = list(emp_data.values())
    potential_employees = {}

    for task_id in tasks_data:
        employments_list.sort(key=lambda emp: emp['active_tasks'])
        min_tasks = employments_list[0]['active_tasks']
        for employee_entry in employments_list:
            emp_id = employee_entry['employee'].id
            """
            If an employee has a parent task with a task_id that matches the given task,
            and the employee has no more than 2 additional active tasks compared to the
            least busy employee, then we add this employee to the list of potential_employees
            """
            if task_id in emp_data[emp_id]['tasks'] and emp_data[emp_id]['active_tasks'] - min_tasks <= 2:
                potential_employees[tasks_data[task_id]] = emp_data[emp_id]['employee']
                employee_entry['active_tasks'] += 1
                break
        """ If the employee hasn't been assigned, then we assign the least busy employee to this task. """
        if not potential_employees.get(tasks_data[task_id]) and employments_list:
            least_busy_employee = employments_list[0]['employee']
            potential_employees[tasks_data[task_id]] = least_busy_employee
            employments_list[0]['active_tasks'] += 1

    return [
        TaskImportantScheme(
            task=TaskScheme(**task.__dict__),
            deadline=task.deadline,
            employees=[potential_employees.get(task.id)],
        )
        for task in important_tasks
    ]
