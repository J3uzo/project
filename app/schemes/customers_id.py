from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemes.deals import SDealGet


class SCustomerIdAddRequest(BaseModel):
    name: str


class SCustomerIdAdd(BaseModel):
    name: str


class SCustomerIdGet(SCustomerIdAdd):
    id: int
    deals: list["SDealGet"] = []


class SCustomerIdPatch(BaseModel):
    name: str | None = None