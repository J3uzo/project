from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel
from datetime import date

if TYPE_CHECKING:
    from app.schemes.customers import SCustomerGet
    from app.schemes.stages import SStageGet
    from app.schemes.reminders import SReminderGet


class SDealAddRequest(BaseModel):
    name: str
    customer_id: int
    amount: float
    stage_id: int
    probability: str
    date: Optional[str] = None
    notes: Optional[str] = None


class SDealAdd(BaseModel):
    name: str
    customer_id: int
    amount: float
    stage_id: int
    probability: str
    date: Optional[str] = None
    notes: Optional[str] = None


class SDealGet(SDealAdd):
    id: int
    customer: Optional["SCustomerGet"] = None
    stage: Optional["SStageGet"] = None
    reminders: list["SReminderGet"] = []


class SDealPatch(BaseModel):
    name: str | None = None
    customer_id: int | None = None
    amount: float | None = None
    stage_id: int | None = None
    probability: str | None = None
    date: str | None = None
    notes: str | None = None