from sqlalchemy.orm import Session

from src.crud.base import BaseCRUD
from src.models import TasksModel
from src.schemas import TaskCreateScheme


class TaskCRUD(BaseCRUD[TasksModel, TaskCreateScheme]):
    """
    CRUD operations for tasks.

    Args:
        BaseCRUD (type): The base CRUD class for performing common operations.
    """

    async def get_important_tasks(self, db: Session) -> list[TasksModel | None]:
        """
        Retrieve a list of important tasks that have no assigned employee but have a parent task.

        Args:
            db (Session): The SQLAlchemy session.

        Returns:
            list[TasksModel | None]: A list of important task instances, or None if no such tasks are found.
        """
        tasks = (db.query(TasksModel).filter(TasksModel.employee_id == None, TasksModel.parent_id != None)).all()
        return tasks


task = TaskCRUD(TasksModel)
