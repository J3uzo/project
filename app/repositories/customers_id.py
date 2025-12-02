from app.repositories.base import BaseRepository
from app.model.customers import CustomerModel
from app.schemes.customers import SCustomerGet

class CustomerRepository(BaseRepository[CustomerModel, SCustomerGet, SCustomerGet, SCustomerGet]):
    model = CustomerModel
    schema = SCustomerGet
    
    def get_with_company(self, db, customer_id: int):
        """Получить клиента с информацией о компании"""
        from app.model.companies import CompanyModel
        customer = db.query(self.model).filter(self.model.id == customer_id).first()
        if not customer:
            return None
        
        result = {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "number": customer.number,
            "company_id": customer.company_id,
            "post": customer.post,
            "tag_id": customer.tag_id,
            "company": None,
            "deals": []
        }
        
        # Информация о компании
        if customer.company_id:
            company = db.query(CompanyModel).filter(CompanyModel.id == customer.company_id).first()
            if company:
                result["company"] = {
                    "id": company.id,
                    "name": company.name,
                    "branch": company.branch,
                    "number": company.number,
                    "email": company.email,
                    "address": company.address,
                    "web": company.web
                }
        
        # Сделки клиента
        from app.model.deals import DealModel
        from app.model.stages import StageModel
        deals = db.query(DealModel).filter(DealModel.customer_id == customer_id).all()
        for deal in deals:
            deal_data = {
                "id": deal.id,
                "name": deal.name,
                "amount": deal.amount,
                "probability": deal.probability,
                "date": deal.date,
                "notes": deal.notes,
                "stage": None
            }
            
            if deal.stage_id:
                stage = db.query(StageModel).filter(StageModel.id == deal.stage_id).first()
                if stage:
                    deal_data["stage"] = {
                        "id": stage.id,
                        "lid": stage.lid,
                        "success": stage.success,
                        "conversation": stage.conversation,
                        "lost": stage.lost
                    }
            
            result["deals"].append(deal_data)
        
        return result
    
    def get_by_company(self, db, company_id: int, skip: int = 0, limit: int = 100):
        """Получить клиентов компании"""
        customers = db.query(self.model).filter(
            self.model.company_id == company_id
        ).offset(skip).limit(limit).all()
        return [self.schema.from_orm(customer) for customer in customers]
    
    def get_by_tag(self, db, tag_id: int, skip: int = 0, limit: int = 100):
        """Получить клиентов по тегу"""
        customers = db.query(self.model).filter(
            self.model.tag_id == tag_id
        ).offset(skip).limit(limit).all()
        return [self.schema.from_orm(customer) for customer in customers]
    
    def search(self, db, search_term: str, skip: int = 0, limit: int = 100):
        """Поиск клиентов по имени, email или телефону"""
        customers = db.query(self.model).filter(
            (self.model.name.like(f"%{search_term}%")) |
            (self.model.email.like(f"%{search_term}%")) |
            (self.model.number.like(f"%{search_term}%"))
        ).offset(skip).limit(limit).all()
        return [self.schema.from_orm(customer) for customer in customers]