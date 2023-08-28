from sqlalchemy import func
from sqlalchemy.orm import Session

from src.crud.base import BaseCRUD
from src.models.employee import EmployeeModel
from src.models.task import StatusEnum, TasksModel
from src.schemas.employee import EmployeeCreateScheme


class EmployeeCRUD(BaseCRUD[EmployeeModel, EmployeeCreateScheme]):
    """
    CRUD operations for employees.

    Args:
        BaseCRUD (type): The base CRUD class for performing common operations.
    """

    async def get_employee_by_name(self, db: Session, employee_name: str) -> EmployeeModel:
        """ Retrieve an employee by their name """
        return db.query(EmployeeModel).filter(EmployeeModel.name == employee_name).first()

    async def busiest_employee(self, db: Session) -> list[tuple[EmployeeModel, ...] | None]:
        """
        Retrieve a list of employees with active tasks (status = doing) in descending order.

        Args:
            db (Session): The SQLAlchemy session.

        Returns:
            list[tuple[EmployeeModel, ...] | None]:
                A list of tuples containing employee instances and their active task counts.
        """
        employees = (
            db.query(EmployeeModel, func.count(TasksModel.id).label('active_task_count'))
            .outerjoin(TasksModel, TasksModel.employee_id == EmployeeModel.id)
            .filter(TasksModel.status == StatusEnum.doing)
            .group_by(EmployeeModel.id)
            .order_by(func.count(TasksModel.id).desc())
        ).all()
        return employees

    async def less_busy_employee(self, db: Session) -> list[tuple[EmployeeModel, ...] | None]:
        """
        Retrieve a list of employees with active tasks in ascending order.

        Args:
            db (Session): The SQLAlchemy session.

        Returns:
            list[tuple[EmployeeModel, ...] | None]:
                A list of tuples containing employee instances and their task counts.
        """
        employees = (
            db.query(EmployeeModel, func.count(TasksModel.id).label('task_count'))
            .outerjoin(TasksModel, EmployeeModel.id == TasksModel.employee_id)
            .group_by(EmployeeModel.id)
            .order_by(func.count(TasksModel.id).asc())
        ).all()
        return employees


employee = EmployeeCRUD(EmployeeModel)
