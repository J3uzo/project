from typing import TYPE_CHECKING

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

if TYPE_CHECKING:
    from app.model.roles import RoleModel


class AdminModel(Base):
    __tablename__ = "admins"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    login: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    pasword: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=False)
    role: Mapped["RoleModel"] = relationship(back_populates="admins")