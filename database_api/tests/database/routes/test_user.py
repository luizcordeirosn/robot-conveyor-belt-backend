import pytest
from fastapi.testclient import TestClient
from main import app
from database.model.user import User
from database.services import user_service
from http import HTTPStatus

client: TestClient = TestClient(app)


@pytest.mark.parametrize(
    "payload, expected_status, expected_response",
    [
        (
            {"name": "Alice", "username": "alice", "password": "senha123"},
            HTTPStatus.OK,
            {"detail": "User created."},
        ),
    ],
)
def test_register_user_success(monkeypatch, payload, expected_status, expected_response):
    """
    Testa se a rota /users cria um novo usuário corretamente.
    """

    def fake_register(user: User):
        assert user.username == payload["username"]
        assert user.name == payload["name"]
        assert user.password == payload["password"]
        return None  # simula sucesso

    monkeypatch.setattr(user_service.UserService, "register", fake_register)

    response = client.post("/users/", json=payload)

    assert response.status_code == expected_status, response.text
    assert response.json() == expected_response


def test_register_user_failure(monkeypatch):
    """
    Testa o comportamento da rota /users quando UserService.register lança exceção.
    """

    def fake_register(user: User):
        raise Exception("Erro when are creating user.")

    monkeypatch.setattr(user_service.UserService, "register", fake_register)

    payload = {"name": "Bob", "username": "bob", "password": "12345"}
    response = client.post("/users/", json=payload)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    body = response.json()
    assert body["detail"] == "Process failed when are creating a new user"
