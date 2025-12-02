from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemes.types import STypeGet
    from app.schemes.contacts import SContactGet
    from app.schemes.deals import SDealGet
    from app.schemes.admins import SAdminGet


class SReminderAddRequest(BaseModel):
    name: str
    description: Optional[str] = None
    date: str
    type_id: int
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None
    admin_id: Optional[int] = None


class SReminderAdd(BaseModel):
    name: str
    description: Optional[str] = None
    date: str
    type_id: int
    contact_id: Optional[int] = None
    deal_id: Optional[int] = None
    admin_id: Optional[int] = None


class SReminderGet(SReminderAdd):
    id: int
    type: Optional["STypeGet"] = None
    contact: Optional["SContactGet"] = None
    deal: Optional["SDealGet"] = None
    admin: Optional["SAdminGet"] = None


class SReminderPatch(BaseModel):
    name: str | None = None
    description: str | None = None
    date: str | None = None
    type_id: int | None = None
    contact_id: int | None = None
    deal_id: int | None = None
    admin_id: int | None = None