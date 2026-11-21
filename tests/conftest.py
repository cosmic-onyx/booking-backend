from collections.abc import Iterator
from datetime import date, datetime, time, timedelta
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import models
from app.db.base import Base
from app.db.session import get_session
from app.main import create_app
from tests import clock


@pytest.fixture(autouse=True)
def frozen_now(monkeypatch: pytest.MonkeyPatch) -> datetime:
    current_moment = datetime.combine(date.today(), time(15, 0))
    monkeypatch.setattr(clock, "now", lambda: current_moment)
    return current_moment


@pytest.fixture
def client() -> Iterator[TestClient]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    def override_get_session() -> Iterator[Session]:
        with session_factory() as session:
            yield session

    app = create_app()
    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def booking_payload() -> dict[str, Any]:
    return {
        "name": "Павел",
        "phone": "+79991234567",
        "booking_date": (date.today() + timedelta(days=1)).isoformat(),
        "booking_time": "18:00:00",
        "guests": 5,
    }
