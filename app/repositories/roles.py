from app.repositories.base import BaseRepository
from app.model.roles import RoleModel
from app.schemes.roles import SRoleGet

class RoleRepository(BaseRepository[RoleModel, SRoleGet, SRoleGet, SRoleGet]):
    model = RoleModel
    schema = SRoleGet
    
    def get_with_admins(self, db, role_id: int):
        """Получить роль с администраторами"""
        from app.model.admins import AdminModel
        
        role = db.query(self.model).filter(self.model.id == role_id).first()
        if not role:
            return None
        
        result = {
            "id": role.id,
            "admin": role.admin,
            "user": role.user,
            "moderator": role.moderator,
            "admins": []
        }
        
        # Администраторы с этой ролью
        admins = db.query(AdminModel).filter(AdminModel.role_id == role_id).all()
        for admin in admins:
            admin_data = {
                "id": admin.id,
                "name": admin.name,
                "login": admin.login
            }
            result["admins"].append(admin_data)
        
        return result
    
    def get_role_by_name(self, db, role_name: str):
        """Получить роль по названию"""
        role = db.query(self.model).filter(
            (self.model.admin == role_name) |
            (self.model.user == role_name) |
            (self.model.moderator == role_name)
        ).first()
        return role