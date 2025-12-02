from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemes.admins import SAdminGet


class SRoleAddRequest(BaseModel):
    admin: Optional[str] = None
    user: Optional[str] = None
    moderator: Optional[str] = None


class SRoleAdd(BaseModel):
    admin: Optional[str] = None
    user: Optional[str] = None
    moderator: Optional[str] = None


class SRoleGet(SRoleAdd):
    id: int
    admins: list["SAdminGet"] = []


class SRolePatch(BaseModel):
    admin: str | None = None
    user: str | None = None
    moderator: str | None = None