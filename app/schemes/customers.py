from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, EmailStr

if TYPE_CHECKING:
    from app.schemes.companies import SCompanyGet
    from app.schemes.tags import STagGet
    from app.schemes.deals import SDealGet


class SCustomerAddRequest(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    number: Optional[str] = None
    company_id: Optional[int] = None
    post: Optional[str] = None
    tag_id: Optional[int] = None


class SCustomerAdd(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    number: Optional[str] = None
    company_id: Optional[int] = None
    post: Optional[str] = None
    tag_id: Optional[int] = None


class SCustomerGet(SCustomerAdd):
    id: int
    company: Optional["SCompanyGet"] = None
    tag: Optional["STagGet"] = None
    deals: list["SDealGet"] = []
    

class SCustomerPatch(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    number: str | None = None
    company_id: int | None = None
    post: str | None = None
    tag_id: int | None = None