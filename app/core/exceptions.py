class BookingError(Exception):
    detail: str = "Booking error"

    def __str__(self) -> str:
        return self.detail


class BookingNotFoundError(BookingError):
    detail = "Booking not found"


class SlotAlreadyBookedError(BookingError):
    detail = "Slot is already booked"
