from typing import TYPE_CHECKING

from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

if TYPE_CHECKING:
    from app.model.types import TypeModel
    from app.model.contacts import ContactModel


class ReminderModel(Base):
    __tablename__ = "reminders"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    data: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    type_id: Mapped[str] = mapped_column(ForeignKey("types.id"), nullable=False)
    type: Mapped["TypeModel"] = relationship(back_populates="types")
    contact_id: Mapped[int] = mapped_column(ForeignKey("contacts.id"), nullable=False)
    contact: Mapped["ContactModel"] = relationship(back_populates="contacts")