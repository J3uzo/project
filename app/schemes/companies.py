from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, EmailStr

if TYPE_CHECKING:
    from app.schemes.customers import SCustomerGet


class SCompanyAddRequest(BaseModel):
    name: str
    branch: Optional[str] = None
    number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    web: Optional[str] = None


class SCompanyAdd(BaseModel):
    name: str
    branch: Optional[str] = None
    number: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    web: Optional[str] = None


class SCompanyGet(SCompanyAdd):
    id: int
    customers: list["SCustomerGet"] = []


class SCompanyPatch(BaseModel):
    name: str | None = None
    branch: str | None = None
    number: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    web: str | None = None