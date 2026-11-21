from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.booking_repository import BookingRepository
from app.services.booking_service import BookingService


def get_booking_service(session: Annotated[Session, Depends(get_session)]) -> BookingService:
    return BookingService(BookingRepository(session))


BookingServiceDep = Annotated[BookingService, Depends(get_booking_service)]
