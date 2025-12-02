from app.repositories.base import BaseRepository
from app.model.stages import StageModel
from app.schemes.stages import SStageGet

class StageRepository(BaseRepository[StageModel, SStageGet, SStageGet, SStageGet]):
    model = StageModel
    schema = SStageGet
    
    def get_with_deals(self, db, stage_id: int):
        """Получить стадию со сделками"""
        from app.model.deals import DealModel
        
        stage = db.query(self.model).filter(self.model.id == stage_id).first()
        if not stage:
            return None
        
        result = {
            "id": stage.id,
            "lid": stage.lid,
            "success": stage.success,
            "conversation": stage.conversation,
            "lost": stage.lost,
            "deals": []
        }
        
        # Сделки на этой стадии
        deals = db.query(DealModel).filter(DealModel.stage_id == stage_id).all()
        for deal in deals:
            deal_data = {
                "id": deal.id,
                "name": deal.name,
                "amount": deal.amount,
                "probability": deal.probability,
                "date": deal.date
            }
            result["deals"].append(deal_data)
        
        return result
    
    def get_stage_by_name(self, db, stage_type: str, stage_name: str):
        """Получить стадию по типу и названию"""
        if stage_type == "lid":
            return db.query(self.model).filter(self.model.lid == stage_name).first()
        elif stage_type == "success":
            return db.query(self.model).filter(self.model.success == stage_name).first()
        elif stage_type == "conversation":
            return db.query(self.model).filter(self.model.conversation == stage_name).first()
        elif stage_type == "lost":
            return db.query(self.model).filter(self.model.lost == stage_name).first()
        return None