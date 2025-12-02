from app.repositories.base import BaseRepository
from app.model.customers_id import Customer_idModel
from app.schemes.customers_id import SCustomerIdGet

class CustomerIdRepository(BaseRepository[Customer_idModel, SCustomerIdGet, SCustomerIdGet, SCustomerIdGet]):
    model = Customer_idModel
    schema = SCustomerIdGet
    
    def get_with_deals(self, db, customer_id_id: int):
        """Получить ID клиента со сделками"""
        from app.model.deals import DealModel
        
        customer_id_obj = db.query(self.model).filter(self.model.id == customer_id_id).first()
        if not customer_id_obj:
            return None
        
        result = {
            "id": customer_id_obj.id,
            "name": customer_id_obj.name,
            "deals": []
        }
        
        # Сделки для этого ID клиента
        deals = db.query(DealModel).filter(DealModel.customer_id == customer_id_obj.id).all()
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