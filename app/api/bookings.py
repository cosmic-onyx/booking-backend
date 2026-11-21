from datetime import date
from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.dependencies import BookingServiceDep
from app.schemas.booking import BookingCreate, BookingRead

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(data: BookingCreate, service: BookingServiceDep) -> BookingRead:
    return service.create(data)


@router.get("", response_model=list[BookingRead])
def list_bookings(
    service: BookingServiceDep,
    booking_date: Annotated[date | None, Query(alias="date")] = None,
) -> list[BookingRead]:
    return service.list_bookings(booking_date)


@router.get("/{booking_id}", response_model=BookingRead)
def get_booking(booking_id: int, service: BookingServiceDep) -> BookingRead:
    return service.get(booking_id)


@router.delete("/{booking_id}", response_model=BookingRead)
def cancel_booking(booking_id: int, service: BookingServiceDep) -> BookingRead:
    return service.cancel(booking_id)
