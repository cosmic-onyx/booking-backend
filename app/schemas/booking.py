from datetime import date, datetime, time, timedelta
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator, model_validator

from app.core.constants import (
    CLOSING_HOUR,
    MAX_DAYS_AHEAD,
    MAX_GUESTS,
    MAX_NAME_LENGTH,
    MIN_GUESTS,
    MIN_NAME_LENGTH,
    OPENING_HOUR,
    PHONE_PATTERN,
)
from app.db.models import BookingStatus

GuestName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=MIN_NAME_LENGTH,
        max_length=MAX_NAME_LENGTH,
    ),
]
PhoneNumber = Annotated[str, StringConstraints(pattern=PHONE_PATTERN)]
GuestsCount = Annotated[int, Field(ge=MIN_GUESTS, le=MAX_GUESTS)]


class BookingCreate(BaseModel):
    name: GuestName
    phone: PhoneNumber
    booking_date: date
    booking_time: time
    guests: GuestsCount

    @field_validator("booking_date")
    @classmethod
    def validate_booking_date(cls, value: date) -> date:
        today = datetime.now().date()
        if not today <= value <= today + timedelta(days=MAX_DAYS_AHEAD):
            raise ValueError(f"Date must be within {MAX_DAYS_AHEAD} days from today and not in the past")
        return value

    @field_validator("booking_time")
    @classmethod
    def validate_booking_time(cls, value: time) -> time:
        is_whole_hour = value.minute == value.second == value.microsecond == 0
        if not (is_whole_hour and OPENING_HOUR <= value.hour <= CLOSING_HOUR):
            raise ValueError(f"Time must be a whole hour from {OPENING_HOUR}:00 to {CLOSING_HOUR}:00")
        return value

    @model_validator(mode="after")
    def validate_booking_is_not_in_the_past(self):
        if datetime.combine(self.booking_date, self.booking_time) < datetime.now():
            raise ValueError("Booking date and time must not be in the past")
        return self


class BookingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    phone: str
    booking_date: date
    booking_time: time
    guests: int
    status: BookingStatus
