from typing import TypeVar, Generic, Type, Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from pydantic import BaseModel
from app.database import get_db
import math

ModelType = TypeVar('ModelType')
SchemaType = TypeVar('SchemaType', bound=BaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseRepository(Generic[ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс репозитория с CRUD операциями"""
    
    def __init__(self, model: Type[ModelType], schema: Type[SchemaType]):
        self.model = model
        self.schema = schema
    
    def get(self, db: Session, id: int) -> Optional[SchemaType]:
        """Получить объект по ID"""
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            return self.schema.from_orm(obj)
        return None
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> List[SchemaType]:
        """Получить несколько объектов с фильтрацией и сортировкой"""
        query = db.query(self.model)
        
        # Применяем фильтры
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    if isinstance(value, str):
                        query = query.filter(getattr(self.model, key).like(f"%{value}%"))
                    else:
                        query = query.filter(getattr(self.model, key) == value)
        
        # Применяем сортировку
        if order_by and hasattr(self.model, order_by):
            if order_desc:
                query = query.order_by(desc(getattr(self.model, order_by)))
            else:
                query = query.order_by(asc(getattr(self.model, order_by)))
        
        # Применяем пагинацию
        query = query.offset(skip).limit(limit)
        
        objects = query.all()
        return [self.schema.from_orm(obj) for obj in objects]
    
    def get_paginated(
        self,
        db: Session,
        page: int = 1,
        per_page: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        order_desc: bool = False
    ) -> Dict[str, Any]:
        """Получить пагинированный список объектов"""
        skip = (page - 1) * per_page
        
        # Получаем общее количество
        count_query = db.query(self.model)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    if isinstance(value, str):
                        count_query = count_query.filter(getattr(self.model, key).like(f"%{value}%"))
                    else:
                        count_query = count_query.filter(getattr(self.model, key) == value)
        total = count_query.count()
        
        # Получаем данные
        data = self.get_multi(db, skip, per_page, filters, order_by, order_desc)
        
        return {
            "data": data,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": math.ceil(total / per_page) if total > 0 else 1
        }
    
    def create(self, db: Session, obj_in: CreateSchemaType) -> SchemaType:
        """Создать новый объект"""
        obj_data = obj_in.dict(exclude_unset=True)
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return self.schema.from_orm(db_obj)
    
    def update(self, db: Session, id: int, obj_in: UpdateSchemaType) -> Optional[SchemaType]:
        """Обновить объект"""
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            return None
        
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.commit()
        db.refresh(db_obj)
        return self.schema.from_orm(db_obj)
    
    def delete(self, db: Session, id: int) -> bool:
        """Удалить объект"""
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            return False
        
        db.delete(db_obj)
        db.commit()
        return True
    
    def count(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """Получить количество объектов"""
        query = db.query(self.model)
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    if isinstance(value, str):
                        query = query.filter(getattr(self.model, key).like(f"%{value}%"))
                    else:
                        query = query.filter(getattr(self.model, key) == value)
        return query.count()