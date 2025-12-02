from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemes.reminders import SReminderGet


class STypeAddRequest(BaseModel):
    bell: Optional[str] = None
    meeting: Optional[str] = None
    next_tep: Optional[str] = None
    other: Optional[str] = None


class STypeAdd(BaseModel):
    bell: Optional[str] = None
    meeting: Optional[str] = None
    next_tep: Optional[str] = None
    other: Optional[str] = None


class STypeGet(STypeAdd):
    id: int
    reminders: list["SReminderGet"] = []


class STypePatch(BaseModel):
    bell: str | None = None
    meeting: str | None = None
    next_tep: str | None = None
    other: str | None = None