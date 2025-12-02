from app.repositories.base import BaseRepository
from app.model.reminders import ReminderModel
from app.schemes.reminders import SReminderGet

class ReminderRepository(BaseRepository[ReminderModel, SReminderGet, SReminderGet, SReminderGet]):
    model = ReminderModel
    schema = SReminderGet
    
    def get_with_relations(self, db, reminder_id: int):
        """Получить напоминание со связанными данными"""
        from app.model.types import TypeModel
        from app.model.contacts import ContactModel
        
        reminder = db.query(self.model).filter(self.model.id == reminder_id).first()
        if not reminder:
            return None
        
        result = {
            "id": reminder.id,
            "name": reminder.name,
            "description": reminder.description,
            "date": reminder.date,
            "type_id": reminder.type_id,
            "contact_id": reminder.contact_id,
            "type": None,
            "contact": None
        }
        
        # Информация о типе
        if reminder.type_id:
            type_obj = db.query(TypeModel).filter(TypeModel.id == reminder.type_id).first()
            if type_obj:
                result["type"] = {
                    "id": type_obj.id,
                    "bell": type_obj.bell,
                    "meeting": type_obj.meeting,
                    "next_tep": type_obj.next_tep,
                    "other": type_obj.other
                }
        
        # Информация о контакте
        if reminder.contact_id:
            contact = db.query(ContactModel).filter(ContactModel.id == reminder.contact_id).first()
            if contact:
                result["contact"] = {
                    "id": contact.id,
                    "name": contact.name
                }
        
        return result
    
    def get_by_contact(self, db, contact_id: int, skip: int = 0, limit: int = 100):
        """Получить напоминания по контакту"""
        reminders = db.query(self.model).filter(
            self.model.contact_id == contact_id
        ).offset(skip).limit(limit).all()
        return [self.schema.from_orm(reminder) for reminder in reminders]
    
    def get_by_type(self, db, type_id: int, skip: int = 0, limit: int = 100):
        """Получить напоминания по типу"""
        reminders = db.query(self.model).filter(
            self.model.type_id == type_id
        ).offset(skip).limit(limit).all()
        return [self.schema.from_orm(reminder) for reminder in reminders]
    
    def get_upcoming(self, db, days: int = 7, skip: int = 0, limit: int = 100):
        """Получить предстоящие напоминания"""
        # Для SQLite используем простой фильтр по дате
        # В реальном приложении здесь была бы более сложная логика
        reminders = db.query(self.model).filter(
            self.model.date != None
        ).offset(skip).limit(limit).all()
        return [self.schema.from_orm(reminder) for reminder in reminders]