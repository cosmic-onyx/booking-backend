from datetime import date, timedelta
from typing import Any

from fastapi.testclient import TestClient


def test_get_booking_by_id(client: TestClient, booking_payload: dict[str, Any]) -> None:
    created = client.post("/bookings", json=booking_payload).json()

    response = client.get(f"/bookings/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_missing_booking_returns_not_found(client: TestClient) -> None:
    response = client.get("/bookings/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Booking not found"}


def test_cancel_booking_keeps_record_with_cancelled_status(
    client: TestClient, booking_payload: dict[str, Any]
) -> None:
    created = client.post("/bookings", json=booking_payload).json()

    cancel_response = client.delete(f"/bookings/{created['id']}")
    get_response = client.get(f"/bookings/{created['id']}")

    assert cancel_response.status_code == 200
    assert cancel_response.json()["status"] == "cancelled"
    assert get_response.json()["status"] == "cancelled"


def test_cancel_missing_booking_returns_not_found(client: TestClient) -> None:
    assert client.delete("/bookings/999").status_code == 404


def test_list_bookings_filters_by_date(client: TestClient, booking_payload: dict[str, Any]) -> None:
    other_date = (date.today() + timedelta(days=2)).isoformat()
    client.post("/bookings", json=booking_payload)
    client.post("/bookings", json={**booking_payload, "booking_date": other_date})

    all_bookings = client.get("/bookings").json()
    filtered = client.get("/bookings", params={"date": other_date}).json()

    assert len(all_bookings) == 2
    assert [booking["booking_date"] for booking in filtered] == [other_date]
