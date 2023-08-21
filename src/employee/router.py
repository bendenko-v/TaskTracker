from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db
from .schemas import EmployeeScheme, EmployeeCreateScheme, EmployeeListResponse
from . import crud

employees_router = APIRouter(prefix='/employee', tags=['employee'])


@employees_router.get('', response_model=list[EmployeeScheme])
def get_employees(db: Session = Depends(get_db)):
    """ Get all employees """
    employees = crud.get_all_employees(db)
    if not employees:
        return JSONResponse(content={'message': 'No tasks found'}, status_code=404)
    return employees


@employees_router.get('/{employee_id}', response_model=EmployeeScheme)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """ Get employee by id """
    employee = crud.get_employee_by_id(db, employee_id)
    if not employee:
        return JSONResponse(content={'message': f'No employee with id {employee_id} found'}, status_code=404)
    return employee


@employees_router.post('')
def create_employee(employee: EmployeeCreateScheme, db: Session = Depends(get_db)):
    """ Create employee """
    if crud.get_employee_by_name(db, employee.name):
        return JSONResponse(
            content={'message': f'Employee with name {employee.name} already exists'}, status_code=400
        )
    return crud.create_employee(db, employee)


@employees_router.put('/{employee_id}')
def update_employee(employee_id: int, data: EmployeeCreateScheme, db: Session = Depends(get_db)):
    """ Update employee """
    return crud.update_employee(db, employee_id, data)


special_router = APIRouter(prefix='/busiest-employee', tags=['busiest-employee'])


@special_router.get('')
def busiest_employee(db: Session = Depends(get_db)) -> EmployeeListResponse:
    """ Get busiest employee """
    return crud.busiest_employee(db)
