from typing import TYPE_CHECKING

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

if TYPE_CHECKING:
    from app.model.roles import RoleModel


class StageModel(Base):
    __tablename__ = "stages"
    id: Mapped[int] = mapped_column(primary_key=True)
    lid: Mapped[str] = mapped_column(String(100), nullable=False)
    success: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    conversation: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    lost: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)