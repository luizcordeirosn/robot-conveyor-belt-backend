from unittest.mock import MagicMock

import pytest
from application.api.routes import robot_route
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def robot_service_mock(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(robot_route, "robot_service", mock)
    return mock


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
