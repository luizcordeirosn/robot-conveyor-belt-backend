from http import HTTPStatus
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_post_login_success():
    """
    Tests the POST /login endpoint when AuthService returns valid user bytes.
    """
    expected_bytes = b"mocked_user_bytes"

    with patch(
        "application.api.routes.auth_route.auth_service.login",
        return_value=expected_bytes,
    ) as mock_login:
        response = client.post("/login", content=b"mock_request_body")

        assert response.status_code == HTTPStatus.OK
        assert response.content == expected_bytes
        assert response.headers["content-type"] == "application/octet-stream"
        mock_login.assert_called_once_with(b"mock_request_body")


def test_post_login_unauthorized():
    """
    Tests the POST /login endpoint when AuthService raises a 401 Unauthorized error.
    """
    with patch(
        "application.api.routes.auth_route.auth_service.login",
        side_effect=HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="User unauthorized."
        ),
    ):
        response = client.post("/login", content=b"invalid_credentials")

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "User unauthorized."}


def test_post_login_internal_error():
    """
    Tests the POST /login endpoint when AuthService raises an unexpected exception.
    """
    with patch(
        "application.api.routes.auth_route.auth_service.login",
        side_effect=Exception("Unexpected error"),
    ):
        with pytest.raises(Exception, match="Unexpected error"):
            client.post("/login", content=b"something_went_wrong")
