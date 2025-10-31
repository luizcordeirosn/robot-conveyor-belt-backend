import pytest
from fastapi.testclient import TestClient
from main import app
from database.model.log import Log
from database.services import log_service
from http import HTTPStatus


client: TestClient = TestClient(app)

@pytest.mark.parametrize(
    "payload, expected_status, expected_response",
    [
        (
            {
                "user_id": 1,
                "category": "reciclável",
                "color": "verde",
                "status": "OK",
            },
            HTTPStatus.OK,
            {"detail": "Log registered."},
        ),
    ],
)
def test_register_log(monkeypatch, payload, expected_status, expected_response):
    """
    Testa criação de log usando monkeypatch no LogService.register
    """

    # Mock da função LogService.register
    def fake_register(log: Log):
        assert log.user_id == payload["user_id"]
        assert log.category == payload["category"]
        assert log.color == payload["color"]
        assert log.status == payload["status"]
        return None

    monkeypatch.setattr(log_service.LogService, "register", fake_register)

    response = client.post("/logs/", json=payload)

    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "user_id, category, expected_logs",
    [
        (1, "reciclável", [{"user_id": 1, "category": "reciclável", "color": "verde", "status": "OK"}])
    ],
)
def test_get_logs_by_category(monkeypatch, user_id, category, expected_logs):
    """
    Testa GET /logs/user/category/{user_id}/{category}
    """

    def fake_get_all_by_category_and_user_id(u_id, cat):
        assert u_id == user_id
        assert cat == category
        return expected_logs

    monkeypatch.setattr(
        log_service.LogService,
        "get_all_by_category_and_user_id",
        fake_get_all_by_category_and_user_id,
    )

    response = client.get(f"/logs/user/category/{user_id}/{category}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_logs


@pytest.mark.parametrize(
    "user_id, color, expected_logs",
    [
        (1, "verde", [{"user_id": 1, "category": "reciclável", "color": "verde", "status": "OK"}])
    ],
)
def test_get_logs_by_color(monkeypatch, user_id, color, expected_logs):
    """
    Testa GET /logs/user/color/{user_id}/{color}
    """

    def fake_get_all_by_color_and_user_id(u_id, col):
        assert u_id == user_id
        assert col == color
        return expected_logs

    monkeypatch.setattr(
        log_service.LogService,
        "get_all_by_color_and_user_id",
        fake_get_all_by_color_and_user_id,
    )

    response = client.get(f"/logs/user/color/{user_id}/{color}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_logs


def test_get_logs_by_user(monkeypatch):
    """
    Testa GET /logs/user/{user_id}
    """
    user_id = 1
    expected_logs = [
        {"user_id": 1, "category": "reciclável", "color": "verde", "status": "OK"}
    ]

    def fake_get_logs_by_user_id(u_id):
        assert u_id == user_id
        return expected_logs

    monkeypatch.setattr(log_service.LogService, "get_logs_by_user_id", fake_get_logs_by_user_id)

    response = client.get(f"/logs/user/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_logs


def test_get_last_execution(monkeypatch):
    """
    Testa GET /logs/user/{user_id}/last-execution/
    """
    user_id = 1
    expected_log = {"user_id": 1, "category": "reciclável", "color": "verde", "status": "OK"}

    def fake_get_last_execution_by_user_id(u_id):
        assert u_id == user_id
        return expected_log

    monkeypatch.setattr(
        log_service.LogService,
        "get_last_execution_by_user_id",
        fake_get_last_execution_by_user_id,
    )

    response = client.get(f"/logs/user/{user_id}/last-execution/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_log
