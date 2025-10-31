from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def requests_post_mock(monkeypatch):
    mock_post = MagicMock()
    monkeypatch.setattr("requests.post", mock_post)
    return mock_post


@pytest.fixture
def requests_put_mock(monkeypatch):
    mock_put = MagicMock()
    monkeypatch.setattr("requests.put", mock_put)
    return mock_put


@pytest.fixture
def requests_get_mock(monkeypatch):
    mock_get = MagicMock()
    monkeypatch.setattr("requests.get", mock_get)
    return mock_get


@pytest.fixture
def requests_post_error(monkeypatch):
    monkeypatch.setattr(
        "requests.post",
        lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Connection error")),
    )


@pytest.fixture
def requests_put_error(monkeypatch):
    monkeypatch.setattr(
        "requests.put",
        lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Connection error")),
    )


@pytest.fixture
def requests_get_error(monkeypatch):
    monkeypatch.setattr(
        "requests.get",
        lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Connection error")),
    )
