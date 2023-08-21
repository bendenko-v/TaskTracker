from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.tasks.models import StatusEnum


class EmployeeCreateScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    job: str


class EmployeeScheme(EmployeeCreateScheme):
    id: int


class TaskResponse(BaseModel):
    name: str
    description: str
    status: StatusEnum
    deadline: datetime
    id: int


class EmployeeResponse(EmployeeScheme):
    active_task_count: int
    tasks: list[TaskResponse]


class EmployeeListResponse(BaseModel):
    employees: list[EmployeeResponse]
