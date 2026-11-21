from typing import Any

from fastapi.testclient import TestClient


def test_create_booking_returns_active_booking(client: TestClient, booking_payload: dict[str, Any]) -> None:
    response = client.post("/bookings", json=booking_payload)

    assert response.status_code == 201
    assert response.json()["status"] == "active"
    assert response.json()["id"] == 1


def test_duplicate_active_slot_returns_conflict(client: TestClient, booking_payload: dict[str, Any]) -> None:
    client.post("/bookings", json=booking_payload)

    response = client.post("/bookings", json=booking_payload)

    assert response.status_code == 409
    assert response.json() == {"detail": "Slot is already booked"}


def test_cancelled_booking_frees_slot(client: TestClient, booking_payload: dict[str, Any]) -> None:
    created = client.post("/bookings", json=booking_payload).json()
    client.delete(f"/bookings/{created['id']}")

    response = client.post("/bookings", json=booking_payload)

    assert response.status_code == 201
    assert response.json()["id"] != created["id"]
