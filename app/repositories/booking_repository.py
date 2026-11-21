from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import SlotAlreadyBookedError
from app.db.models import Booking


class BookingRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, booking: Booking) -> Booking:
        self._session.add(booking)
        self._commit()
        return booking

    def get_by_id(self, booking_id: int) -> Booking | None:
        return self._session.get(Booking, booking_id)

    def list_all(self, booking_date: date | None = None) -> list[Booking]:
        query = select(Booking).order_by(Booking.booking_date, Booking.booking_time, Booking.id)
        if booking_date is not None:
            query = query.where(Booking.booking_date == booking_date)
        return list(self._session.scalars(query))

    def save(self, booking: Booking) -> Booking:
        self._commit()
        return booking

    def _commit(self) -> None:
        try:
            self._session.commit()
        except IntegrityError as error:
            self._session.rollback()
            raise SlotAlreadyBookedError from error
