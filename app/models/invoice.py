from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Invoice(Base):
    __tablename__ = 'invoices'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(100))
    total: Mapped[float] = mapped_column(Float)
    invoice_date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(100))
    active: Mapped[bool] = mapped_column(Boolean)
