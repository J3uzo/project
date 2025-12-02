from typing import TYPE_CHECKING

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

if TYPE_CHECKING:
    from app.model.roles import RoleModel


class TagModel(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    VIP: Mapped[str] = mapped_column(String(100), nullable=False)
    activ: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    partner: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)