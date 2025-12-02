from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

if TYPE_CHECKING:
    from app.schemes.roles import SRoleGet


class SAdminAddRequest(BaseModel):
    name: str
    login: str
    password: str
    role_id: Optional[int] = None


class SAdminAdd(BaseModel):
    name: str
    login: str
    pasword: str
    role_id: Optional[int] = None


class SAdminAuth(BaseModel):
    login: str
    password: str


class SAdminGet(SAdminAdd):
    id: int
    role: Optional["SRoleGet"] = None


class SAdminPatch(BaseModel):
    name: str | None = None
    login: str | None = None
    password: str | None = None
    role_id: int | None = None