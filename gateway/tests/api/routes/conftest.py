from unittest.mock import MagicMock

import pytest
from application.api.routes import (
    auth_route,
    conveyor_belt_route,
    database_route,
    user_route,
)


@pytest.fixture
def auth_route_mock(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(auth_route, "auth_service", mock)
    return mock


@pytest.fixture
def conveyor_belt_route_mock(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(conveyor_belt_route, "conveyor_belt_service", mock)
    return mock


@pytest.fixture
def database_route_mock(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(database_route, "database_service", mock)
    return mock


@pytest.fixture
def user_route_mock(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(user_route, "user_service", mock)
    return mock
