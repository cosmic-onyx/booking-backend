from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import BookingNotFoundError, SlotAlreadyBookedError


def _build_handler(status_code: int):
    async def handler(_: Request, error: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"detail": str(error)})

    return handler


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BookingNotFoundError, _build_handler(status.HTTP_404_NOT_FOUND))
    app.add_exception_handler(SlotAlreadyBookedError, _build_handler(status.HTTP_409_CONFLICT))
