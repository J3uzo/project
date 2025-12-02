from typing import TYPE_CHECKING

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

if TYPE_CHECKING:
    from app.model.roles import RoleModel


class RoleModel(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    admin: Mapped[str] = mapped_column(String(100), nullable=False)
    user: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    moderator: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)