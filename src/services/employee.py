from fastapi import HTTPException

from src.models import EmployeeModel, StatusEnum
from src.schemas import TaskResponse, EmployeeResponse, EmployeeListResponse


def get_busiest_employee(employees: list[tuple[EmployeeModel, ...] | None]) -> EmployeeListResponse:
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
