from app.repositories.base import BaseRepository
from app.model.companies import CompanyModel
from app.schemes.companies import SCompanyGet

class CompanyRepository(BaseRepository[CompanyModel, SCompanyGet, SCompanyGet, SCompanyGet]):
    model = CompanyModel
    schema = SCompanyGet
    
    def get_with_customers(self, db, company_id: int):
        """Получить компанию с клиентами"""
        from app.model.customers import CustomerModel
        
        company = db.query(self.model).filter(self.model.id == company_id).first()
        if not company:
            return None
        
        result = {
            "id": company.id,
            "name": company.name,
            "branch": company.branch,
            "number": company.number,
            "email": company.email,
            "address": company.address,
            "web": company.web,
            "customers": []
        }
        
        # Клиенты компании
        customers = db.query(CustomerModel).filter(
            CustomerModel.company_id == company_id
        ).all()
        
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
    
    def search(self, db, search_term: str, skip: int = 0, limit: int = 100):
        """Поиск компаний"""
        companies = db.query(self.model).filter(
            (self.model.name.like(f"%{search_term}%")) |
            (self.model.branch.like(f"%{search_term}%")) |
            (self.model.email.like(f"%{search_term}%"))
        ).offset(skip).limit(limit).all()
        return [self.schema.from_orm(company) for company in companies]
    
    def get_by_industry(self, db, industry: str, skip: int = 0, limit: int = 100):
        """Получить компании по отрасли"""
        companies = db.query(self.model).filter(
            self.model.branch.like(f"%{industry}%")
        ).offset(skip).limit(limit).all()
        return [self.schema.from_orm(company) for company in companies]