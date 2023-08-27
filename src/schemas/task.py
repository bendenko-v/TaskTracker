from datetime import datetime

from pydantic import BaseModel

from src.models.task import StatusEnum
from src.schemas import EmployeeScheme


class TaskCreateScheme(BaseModel):
    name: str
    description: str
    status: StatusEnum
    employee_id: int | None = None
    parent_id: int | None = None
    deadline: datetime | None = None


class TaskScheme(TaskCreateScheme):
    id: int


class TaskImportantScheme(BaseModel):
    task: TaskScheme
    deadline: datetime
    employees: list[EmployeeScheme]
