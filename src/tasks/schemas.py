from datetime import datetime

from pydantic import BaseModel

from ..employee.schemas import EmployeeScheme
from .models import StatusEnum


class TaskCreateScheme(BaseModel):
    name: str
    description: str
    status: StatusEnum
    employee_id: int
    parent_id: int
    deadline: datetime


class TaskScheme(TaskCreateScheme):
    id: int


class TaskImportantScheme(BaseModel):
    task: TaskScheme
    deadline: datetime
    employees: list[EmployeeScheme]
