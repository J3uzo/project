from typing import TYPE_CHECKING

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

if TYPE_CHECKING:
    from app.model.roles import RoleModel


class TypeModel(Base):
    __tablename__ = "types"
    id: Mapped[int] = mapped_column(primary_key=True)
    bell: Mapped[str] = mapped_column(String(100), nullable=False)
    meeting: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    next_tep: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    other: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)