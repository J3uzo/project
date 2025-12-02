from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.schemes.deals import SDealGet


class SStageAddRequest(BaseModel):
    lid: Optional[str] = None
    success: Optional[str] = None
    conversation: Optional[str] = None
    lost: Optional[str] = None


class SStageAdd(BaseModel):
    lid: Optional[str] = None
    success: Optional[str] = None
    conversation: Optional[str] = None
    lost: Optional[str] = None


class SStageGet(SStageAdd):
    id: int
    deals: list["SDealGet"] = []


class SStagePatch(BaseModel):
    lid: str | None = None
    success: str | None = None
    conversation: str | None = None
    lost: str | None = None