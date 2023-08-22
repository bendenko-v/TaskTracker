from datetime import datetime

from pydantic import BaseModel

from ..employee.schemas import EmployeeScheme
from .models import StatusEnum


class TaskCreateScheme(BaseModel):
    name: str
    description: str
    status: StatusEnum
    employee_id: int | None = None
    parent_id: int
    deadline: datetime | None = None


class TaskScheme(TaskCreateScheme):
    id: int


class TaskImportantScheme(BaseModel):
    task: TaskScheme
    deadline: datetime
    employees: list[EmployeeScheme]
