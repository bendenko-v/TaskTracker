from sqlalchemy import Column, Integer, String

from src.database import Base


class EmployeeModel(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    job = Column(String(255), nullable=False)
