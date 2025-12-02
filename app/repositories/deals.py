from app.repositories.base import BaseRepository
from app.model.deals import DealModel
from app.schemes.deals import SDealGet

class DealRepository(BaseRepository[DealModel, SDealGet, SDealGet, SDealGet]):
    model = DealModel
    schema = SDealGet
    
    def get_with_relations(self, db, deal_id: int):
        """Получить сделку со связанными данными"""
        from app.model.customers import CustomerModel
        from app.model.stages import StageModel
        from app.model.reminders import ReminderModel
        from app.model.customers_id import CustomerIdModel
        
        deal = db.query(self.model).filter(self.model.id == deal_id).first()
        if not deal:
            return None
        
        result = {
            "id": deal.id,
            "name": deal.name,
            "customer_id": deal.customer_id,
            "amount": deal.amount,
            "stage_id": deal.stage_id,
            "probability": deal.probability,
            "date": deal.date,
            "notes": deal.notes,
            "customer": None,
            "stage": None,
            "reminders": []
        }
        
        # Информация о клиенте
        if deal.customer_id:
            customer = db.query(CustomerModel).filter(CustomerModel.id == deal.customer_id).first()
            if customer:
                result["customer"] = {
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "number": customer.number,
                    "post": customer.post
                }
        
        # Информация о стадии
        if deal.stage_id:
            stage = db.query(StageModel).filter(StageModel.id == deal.stage_id).first()
            if stage:
                result["stage"] = {
                    "id": stage.id,
                    "lid": stage.lid,
                    "success": stage.success,
                    "conversation": stage.conversation,
                    "lost": stage.lost
                }
        
        # Напоминания по сделке
        reminders = db.query(ReminderModel).filter(ReminderModel.id == deal.id).all()
        for reminder in reminders:
            reminder_data = {
                "id": reminder.id,
                "name": reminder.name,
                "description": reminder.description,
                "date": reminder.date,
                "type_id": reminder.type_id,
                "contact_id": reminder.contact_id
            }
            result["reminders"].append(reminder_data)
        
        return result
    
    def get_by_stage(self, db, stage_id: int, skip: int = 0, limit: int = 100):
        """Получить сделки по стадии"""
        deals = db.query(self.model).filter(
            self.model.stage_id == stage_id
        ).offset(skip).limit(limit).all()
        return [self.schema.from_orm(deal) for deal in deals]
    
    def get_by_customer(self, db, customer_id: int, skip: int = 0, limit: int = 100):
        """Получить сделки клиента"""
        deals = db.query(self.model).filter(
            self.model.customer_id == customer_id
        ).offset(skip).limit(limit).all()
        return [self.schema.from_orm(deal) for deal in deals]
    
    def get_summary(self, db):
        """Получить сводку по сделкам"""
        from sqlalchemy import func
        
        # Общая статистика
        total_query = db.query(
            func.count(self.model.id).label('total_count'),
            func.sum(self.model.amount).label('total_amount')
        ).first()
        
        # Статистика по стадиям
        from app.model.stages import StageModel
        stages_stats = db.query(
            StageModel.lid.label('stage_name'),
            func.count(self.model.id).label('deal_count'),
            func.sum(self.model.amount).label('deal_amount')
        ).join(
            self.model, self.model.stage_id == StageModel.id
        ).group_by(StageModel.lid).all()
        
        # Конвертируем в словарь
        stages_data = []
        for stat in stages_stats:
            stages_data.append({
                "stage": stat.stage_name or "Без стадии",
                "count": stat.deal_count or 0,
                "amount": stat.deal_amount or 0
            })
        
        return {
            "total_count": total_query.total_count or 0,
            "total_amount": total_query.total_amount or 0,
            "stages": stages_data
        }