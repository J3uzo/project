from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemes.reminders import SReminderGet


class SContactAddRequest(BaseModel):
    name: str


class SContactAdd(BaseModel):
    name: str


class SContactGet(SContactAdd):
    id: int
    reminders: list["SReminderGet"] = []


class SContactPatch(BaseModel):
    name: str | None = None