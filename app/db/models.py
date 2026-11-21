from datetime import date, time
from enum import StrEnum

from sqlalchemy import Enum, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.constants import MAX_NAME_LENGTH, PHONE_LENGTH
from app.db.base import Base


class BookingStatus(StrEnum):
    ACTIVE = "active"
    CANCELLED = "cancelled"


class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (
        Index(
            "uq_bookings_active_slot",
            "booking_date",
            "booking_time",
            unique=True,
            sqlite_where=text("status = 'active'"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH))
    phone: Mapped[str] = mapped_column(String(PHONE_LENGTH))
    booking_date: Mapped[date]
    booking_time: Mapped[time]
    guests: Mapped[int]
    status: Mapped[BookingStatus] = mapped_column(
        Enum(
            BookingStatus,
            native_enum=False,
            length=16,
            values_callable=lambda statuses: [status.value for status in statuses],
        ),
        default=BookingStatus.ACTIVE,
    )
