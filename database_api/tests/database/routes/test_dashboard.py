import pytest
from fastapi.testclient import TestClient
from main import app
from database.model.dashboard import Dashboard
from database.services import dashboard_service
from http import HTTPStatus

client: TestClient = TestClient(app)


@pytest.mark.parametrize(
    "payload, expected_status, expected_response",
    [
        (
            # Caso 1: dashboard válido
            {
                "user_id": 1,
                "image": "image1.png",
                "label": 1,
                "confidence": 98.5,
            },
            HTTPStatus.OK,
            {"detail": "Dashboard registered successfully."},
        ),
    ],
)
def test_register_dashboard(monkeypatch, payload, expected_status, expected_response):
    """
    Testa criação de dashboard usando monkeypatch no DashboardService.register
    """

    def fake_register(dashboard: Dashboard):
        assert dashboard.user_id == payload["user_id"]
        assert dashboard.image == payload["image"]
        assert dashboard.label == payload["label"]
        assert dashboard.confidence == payload["confidence"]
        return None

    monkeypatch.setattr(dashboard_service.DashboardService, "register", fake_register)

    response = client.post("/dashboards/", json=payload)
    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "user_id, expected_dashboards",
    [
        (
            1,
            [
                {"user_id": 1, "image": "image1.png", "label": 1, "confidence": 98.5},
                {"user_id": 1, "image": "image2.png", "label": 2, "confidence": 90.0},
            ],
        ),
    ],
)
def test_get_dashboards_by_user(monkeypatch, user_id, expected_dashboards):
    """
    Testa GET /dashboards/user/{user_id}
    """

    def fake_get_all_by_user_id(u_id):
        assert u_id == user_id
        return expected_dashboards

    monkeypatch.setattr(
        dashboard_service.DashboardService,
        "get_all_by_user_id",
        fake_get_all_by_user_id,
    )

    response = client.get(f"/dashboards/user/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected_dashboards


@pytest.mark.parametrize(
    "user_id, label, expected_dashboards",
    [
        (
            1,
            1,
            [
                {"user_id": 1, "image": "image1.png", "label": 1, "confidence": 98.5},
            ],
        ),
    ],
)
def test_get_dashboards_by_label(monkeypatch, user_id, label, expected_dashboards):
    """
    Testa GET /dashboards/label/{user_id}/{label}
    """

    def fake_service(u_id, lbl):
        assert u_id == user_id
        assert lbl == label
        return {"data": expected_dashboards}

    monkeypatch.setattr(dashboard_service.DashboardService,
        "get_all_by_label_and_user_id", fake_service)

    response = client.get(f"/dashboards/label/{user_id}/{label}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"data": expected_dashboards}
