from typing import TYPE_CHECKING

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

if TYPE_CHECKING:
    from app.model.companies import CompanyModel
    from app.model.tags import TagModel


class CompanyModel(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    branch: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    addres: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    web: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)