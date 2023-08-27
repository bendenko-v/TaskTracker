from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateUpdateSchemaType = TypeVar('CreateUpdateSchemaType', bound=BaseModel)


class BaseCRUD(Generic[ModelType, CreateUpdateSchemaType]):
    """
    Base CRUD class with default methods to create, read and update in
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(self, db: Session) -> list[tuple[ModelType, ...]]:
        return db.query(self.model).all()

    async def get_by_id(self, db: Session, item_id: int) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == item_id).first()

    async def create(self, db: Session, data: CreateUpdateSchemaType) -> ModelType:
        item = self.model(**data.model_dump())
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    async def update(self, db: Session, item_id: int, data: CreateUpdateSchemaType) -> ModelType | str:
        item = await self.get_by_id(db, item_id)
        if not item:
            return 'Item not found'
        try:
            for key, value in data.model_dump().items():
                setattr(item, key, value)
            db.commit()
            db.refresh(item)
            return item
        except IntegrityError as e:
            return str(e)
