from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemes.customers import SCustomerGet


class STagAddRequest(BaseModel):
    VIP: Optional[str] = None
    activ: Optional[str] = None
    partner: Optional[str] = None


class STagAdd(BaseModel):
    VIP: Optional[str] = None
    activ: Optional[str] = None
    partner: Optional[str] = None


class STagGet(STagAdd):
    id: int
    customers: list["SCustomerGet"] = []


class STagPatch(BaseModel):
    VIP: str | None = None
    activ: str | None = None
    partner: str | None = None