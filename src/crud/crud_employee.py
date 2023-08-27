from sqlalchemy import func
from sqlalchemy.orm import Session

from ..crud.base import BaseCRUD
from ..models.employee import EmployeeModel
from ..models.task import StatusEnum, TasksModel
from ..schemas.employee import EmployeeCreateScheme


class EmployeeCRUD(BaseCRUD[EmployeeModel, EmployeeCreateScheme]):
    """
    CRUD for employees
    """

    def get_employee_by_name(self, db: Session, employee_name: str) -> EmployeeModel:
        return db.query(EmployeeModel).filter(EmployeeModel.name == employee_name).first()

    def busiest_employee(self, db: Session) -> list[tuple[EmployeeModel, ...] | None]:
        # Get employees with active tasks (status = doing) in descending order """
        employees = (
            db.query(EmployeeModel, func.count(TasksModel.id).label('active_task_count'))
            .outerjoin(TasksModel, TasksModel.employee_id == EmployeeModel.id)
            .filter(TasksModel.status == StatusEnum.doing)
            .group_by(EmployeeModel.id)
            .order_by(func.count(TasksModel.id).desc())
        ).all()
        return employees

    def less_busy_employee(self, db: Session) -> list[tuple[EmployeeModel, ...] | None]:
        # Get employees with active tasks in ascending order """
        employees = (
            db.query(EmployeeModel, func.count(TasksModel.id).label('task_count'))
            .outerjoin(TasksModel, EmployeeModel.id == TasksModel.employee_id)
            .group_by(EmployeeModel.id)
            .order_by(func.count(TasksModel.id).asc())
        ).all()
        return employees


employee = EmployeeCRUD(EmployeeModel)
