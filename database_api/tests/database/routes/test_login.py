import pytest
from fastapi.testclient import TestClient
from database.services import user_service
from main import app
from database.model.user import User
from database.connection import connection
from database.proto.auth import PotentialUser

from http import HTTPStatus
import bcrypt

client = TestClient(app)


@pytest.fixture
def login_user(session):
    """Usuário de teste"""
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(b"senha123", salt)

    user = User(
        name="Test User",
        username="test_login",
        password=hash_password.decode("utf-8"),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_login_success(monkeypatch, session, login_user):
    """
    Testa o login com credenciais corretas
    """

    monkeypatch.setattr(
        'database.dao.user_dao.get_session',
        lambda: session
    )

    response = client.post(
        "/login/",
        json={
            "username": login_user.username,
            "password": "senha123",
        },
    )

    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body["username"] == login_user.username


def test_login_invalid_credentials(monkeypatch, session):
    """
    Testa login com credenciais inválidas.
    """

    response = client.post(
        "/login/",
        json={
            "username": "fake_user",
            "password": "senha_errada",
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["detail"] == "User unauthorized."

