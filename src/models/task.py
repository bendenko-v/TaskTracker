import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base

from .employee import EmployeeModel


class StatusEnum(enum.Enum):
    todo = 'todo'
    doing = 'doing'
    done = 'done'


class TasksModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.todo)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    parent_id = Column(Integer, ForeignKey('tasks.id'))
    deadline = Column(DateTime(timezone=True), nullable=True)

    employee = relationship(EmployeeModel, backref='tasks')
    parent = relationship('TasksModel', remote_side=id, backref='children')
