from datetime import date

from app.core.exceptions import BookingNotFoundError
from app.db.models import Booking, BookingStatus
from app.repositories.booking_repository import BookingRepository
from app.schemas.booking import BookingCreate


class BookingService:
    def __init__(self, repository: BookingRepository) -> None:
        self._repository = repository

    def create(self, data: BookingCreate) -> Booking:
        booking = Booking(**data.model_dump(), status=BookingStatus.ACTIVE)
        return self._repository.add(booking)

    def list_bookings(self, booking_date: date | None = None) -> list[Booking]:
        return self._repository.list_all(booking_date)

    def get(self, booking_id: int) -> Booking:
        booking = self._repository.get_by_id(booking_id)
        if booking is None:
            raise BookingNotFoundError
        return booking

    def cancel(self, booking_id: int) -> Booking:
        booking = self.get(booking_id)
        booking.status = BookingStatus.CANCELLED
        return self._repository.save(booking)
