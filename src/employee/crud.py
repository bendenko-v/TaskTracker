from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from .models import EmployeeModel
from ..tasks.models import TasksModel, StatusEnum
from .schemas import EmployeeCreateScheme, EmployeeResponse, EmployeeListResponse, TaskResponse


def get_all_employees(db: Session) -> list[EmployeeModel]:
    return db.query(EmployeeModel).all()


def get_employee_by_id(db: Session, employee_id: int) -> EmployeeModel:
    return db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()


def get_employee_by_name(db: Session, employee_name: str) -> EmployeeModel:
    return db.query(EmployeeModel).filter(EmployeeModel.name == employee_name).first()


def create_employee(db: Session, data: EmployeeCreateScheme) -> JSONResponse:
    try:
        employee = EmployeeModel(**data.model_dump())
        db.add(employee)
        db.commit()
    except ValidationError as err:
        raise HTTPException(status_code=400, detail=err.messages)
    return JSONResponse(content={'message': 'Employee created'}, status_code=status.HTTP_201_CREATED)


def update_employee(db: Session, employee_id: int, data: EmployeeCreateScheme) -> JSONResponse:
    try:
        db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).update(data.model_dump())
        db.commit()
    except ValidationError as err:
        raise HTTPException(status_code=400, detail=err.messages)
    return JSONResponse(content={'message': 'Employee data updated'}, status_code=status.HTTP_204_NO_CONTENT)


def busiest_employee(db: Session) -> EmployeeListResponse:
    employees = (
        db.query(EmployeeModel, func.count(TasksModel.id).label('active_task_count'))
        .outerjoin(TasksModel, TasksModel.employee_id == EmployeeModel.id)
        .filter(TasksModel.status == StatusEnum.doing)
        .group_by(EmployeeModel.id)
        .order_by(func.count(TasksModel.id).desc())
    ).all()

    if not employees:
        raise HTTPException(status_code=404, detail='Employees not found')

    response_data = [
        EmployeeResponse(
            **employee.__dict__,
            active_task_count=active_task_count,
            tasks=[
                TaskResponse(**task.__dict__) for task in employee.tasks if task.status == StatusEnum.doing
            ]
        )
        for employee, active_task_count in employees
    ]

    return EmployeeListResponse(employees=response_data)
