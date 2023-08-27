from sqlalchemy.orm import Session

from src.crud.base import BaseCRUD
from src.models import TasksModel
from src.schemas import TaskCreateScheme


class TaskCRUD(BaseCRUD[TasksModel, TaskCreateScheme]):
    """
    CRUD for tasks
    """

    def get_important_tasks(self, db: Session) -> list[TasksModel | None]:
        # Get important tasks (tasks has parent and no employee assigned) """
        tasks = (
            db.query(TasksModel)
            .filter(TasksModel.employee_id == None, TasksModel.parent_id != None)
        ).all()
        return tasks


task = TaskCRUD(TasksModel)
