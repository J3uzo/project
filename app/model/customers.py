from typing import TYPE_CHECKING

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

if TYPE_CHECKING:
    from app.model.companies import CompanyModel
    from app.model.tags import TagModel


class CustomerModel(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    number: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    company: Mapped["CompanyModel"] = relationship(back_populates="customers")
    tags_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), nullable=False)
    tag: Mapped["TagModel"] = relationship(back_populates="customers")