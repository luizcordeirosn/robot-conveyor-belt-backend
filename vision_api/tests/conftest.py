from unittest.mock import MagicMock

import pytest
from application.api.routes import camera_route
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def camera_service_mock(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr(camera_route, "camera_service", mock)
    return mock


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
