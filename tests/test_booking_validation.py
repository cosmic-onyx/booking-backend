from datetime import date, timedelta
from typing import Any

import pytest
from fastapi.testclient import TestClient


def _post_with(client: TestClient, payload: dict[str, Any], **overrides: Any) -> int:
    return client.post("/bookings", json={**payload, **overrides}).status_code


@pytest.mark.parametrize(
    "days_offset, expected_status",
    [(-1, 422), (0, 422), (30, 201), (31, 422)],
)
def test_booking_date_must_be_within_allowed_range(
    client: TestClient, booking_payload: dict[str, Any], days_offset: int, expected_status: int
) -> None:
    booking_date = (date.today() + timedelta(days=days_offset)).isoformat()

    assert _post_with(client, booking_payload, booking_date=booking_date) == expected_status


@pytest.mark.parametrize(
    "booking_time, expected_status",
    [("11:00:00", 422), ("12:00:00", 201), ("22:00:00", 201), ("23:00:00", 422), ("15:30:00", 422)],
)
def test_booking_time_must_be_whole_hour_within_working_hours(
    client: TestClient, booking_payload: dict[str, Any], booking_time: str, expected_status: int
) -> None:
    assert _post_with(client, booking_payload, booking_time=booking_time) == expected_status


@pytest.mark.parametrize(
    "phone, expected_status",
    [("+79991234567", 201), ("89991234567", 422), ("+7999123456", 422), ("+799912345678", 422), ("+7999abc4567", 422)],
)
def test_phone_must_match_format(
    client: TestClient, booking_payload: dict[str, Any], phone: str, expected_status: int
) -> None:
    assert _post_with(client, booking_payload, phone=phone) == expected_status


@pytest.mark.parametrize(
    "guests, expected_status",
    [(0, 422), (1, 201), (10, 201), (11, 422)],
)
def test_guests_must_be_between_one_and_ten(
    client: TestClient, booking_payload: dict[str, Any], guests: int, expected_status: int
) -> None:
    assert _post_with(client, booking_payload, guests=guests) == expected_status


@pytest.mark.parametrize(
    "name, expected_status",
    [("A", 422), ("Ян", 201), ("А" * 50, 201), ("А" * 51, 422)],
)
def test_name_length_must_be_between_two_and_fifty(
    client: TestClient, booking_payload: dict[str, Any], name: str, expected_status: int
) -> None:
    assert _post_with(client, booking_payload, name=name) == expected_status


@pytest.mark.parametrize(
    "days_offset, booking_time, expected_status",
    [(0, "14:00:00", 422), (0, "16:00:00", 422), (1, "12:00:00", 201)],
)
def test_booking_datetime_must_not_be_in_the_past(
    client: TestClient,
    booking_payload: dict[str, Any],
    days_offset: int,
    booking_time: str,
    expected_status: int,
) -> None:
    booking_date = (date.today() + timedelta(days=days_offset)).isoformat()

    status_code = _post_with(client, booking_payload, booking_date=booking_date, booking_time=booking_time)

    assert status_code == expected_status
