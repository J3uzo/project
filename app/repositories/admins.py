from app.repositories.base import BaseRepository
from app.model.admins import AdminModel
from app.schemes.admins import SAdminGet

class AdminRepository(BaseRepository[AdminModel, SAdminGet, SAdminGet, SAdminGet]):
    model = AdminModel
    schema = SAdminGet
    
    def get_by_login(self, db, login: str):
        """Получить администратора по логину"""
        admin = db.query(self.model).filter(self.model.login == login).first()
        if admin:
            return self.schema.from_orm(admin)
        return None
    
    def authenticate(self, db, login: str, password: str):
        """Аутентификация администратора"""
        admin = db.query(self.model).filter(
            self.model.login == login,
            self.model.pasword == password
        ).first()
        if admin:
            return self.schema.from_orm(admin)
        return None
    
    def get_with_role(self, db, admin_id: int):
        """Получить администратора с информацией о роли"""
        from app.model.roles import RoleModel
        admin = db.query(self.model).filter(self.model.id == admin_id).first()
        if not admin:
            return None
        
        result = {
            "id": admin.id,
            "name": admin.name,
            "login": admin.login,
            "role_id": admin.role_id,
            "role": None
        }
        
        if admin.role_id:
            role = db.query(RoleModel).filter(RoleModel.id == admin.role_id).first()
            if role:
                result["role"] = {
                    "id": role.id,
                    "admin": role.admin,
                    "user": role.user,
                    "moderator": role.moderator
                }
        
        return result