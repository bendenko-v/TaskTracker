from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.crud.crud_employee import employee as crud
from src.database import get_db
from src.schemas import EmployeeCreateScheme, EmployeeListResponse, EmployeeScheme
from src.services import get_busiest_employee

router = APIRouter()


@router.get('/busiest', response_model=EmployeeListResponse)
async def busiest_employee(db: Session = Depends(get_db)) -> EmployeeListResponse:
    """Get busiest employee"""
    if employees := await get_busiest_employee(employees=await crud.busiest_employee(db)):
        return employees
    else:
        raise HTTPException(status_code=404, detail='Employees not found')


@router.get('/', response_model=list[EmployeeScheme])
async def get_employees(db: Session = Depends(get_db)):
    """Retrieve all employees"""
    employees = await crud.get_all(db)
    if not employees:
        raise HTTPException(status_code=404, detail='Employees not found')
    return employees


@router.get('/{employee_id}', response_model=EmployeeScheme)
async def get_employee(employee_id: int, db: Session = Depends(get_db)):
    """Get employee by id"""
    employee = await crud.get_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail=f'Employee with id {employee_id} not found')
    return employee


@router.post('')
async def create_employee(employee: EmployeeCreateScheme, db: Session = Depends(get_db)):
    """Create employee"""
    if await crud.get_employee_by_name(db, employee.name):
        raise HTTPException(status_code=400, detail=f'Employee with name {employee.name} already exists')
    return await crud.create(db, employee)


@router.put('/{employee_id}')
async def update_employee(employee_id: int, data: EmployeeCreateScheme, db: Session = Depends(get_db)):
    """Update employee"""
    employee_updated = await crud.update(db, employee_id, data)
    if isinstance(employee_updated, str):
        raise HTTPException(status_code=400, detail=employee_updated)
    else:
        return employee_updated
