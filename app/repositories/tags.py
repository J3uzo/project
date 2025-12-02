from app.repositories.base import BaseRepository
from app.model.tags import TagModel
from app.schemes.tags import STagGet

class TagRepository(BaseRepository[TagModel, STagGet, STagGet, STagGet]):
    model = TagModel
    schema = STagGet
    
    def get_with_customers(self, db, tag_id: int):
        """Получить тег с клиентами"""
        from app.model.customers import CustomerModel
        
        tag = db.query(self.model).filter(self.model.id == tag_id).first()
        if not tag:
            return None
        
        result = {
            "id": tag.id,
            "VIP": tag.VIP,
            "activ": tag.activ,
            "partner": tag.partner,
            "customers": []
        }
        
        # Клиенты с этим тегом
        customers = db.query(CustomerModel).filter(CustomerModel.tag_id == tag_id).all()
        for customer in customers:
            customer_data = {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "number": customer.number,
                "post": customer.post
            }
            result["customers"].append(customer_data)
        
        return result
    
    def get_tag_by_type(self, db, tag_type: str, tag_value: str):
        """Получить тег по типу и значению"""
        if tag_type == "VIP":
            return db.query(self.model).filter(self.model.VIP == tag_value).first()
        elif tag_type == "activ":
            return db.query(self.model).filter(self.model.activ == tag_value).first()
        elif tag_type == "partner":
            return db.query(self.model).filter(self.model.partner == tag_value).first()
        return None
    
    def get_vip_tags(self, db):
        """Получить все VIP теги"""
        return db.query(self.model).filter(self.model.VIP.isnot(None)).all()
    
    def get_active_tags(self, db):
        """Получить все активные теги"""
        return db.query(self.model).filter(self.model.activ.isnot(None)).all()