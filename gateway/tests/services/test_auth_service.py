import pytest
from fastapi import HTTPException


def test_auth_service_login_success(
    auth_service_mock, potential_user_bytes, requests_post_success
):
    """
    Tests successful login returns bytes from Mapper.
    """
    result_bytes = auth_service_mock.login(potential_user_bytes)
    assert result_bytes == b"mocked_bytes"


def test_auth_service_login_unauthorized(
    auth_service_mock, potential_user_bytes, requests_post_unauthorized
):
    """
    Tests login when the server returns 401 Unauthorized.
    """
    with pytest.raises(HTTPException) as exc_info:
        auth_service_mock.login(potential_user_bytes)
    assert exc_info.value.status_code == 401


def test_auth_service_login_server_error(
    auth_service_mock, potential_user_bytes, requests_post_server_error
):
    """
    Tests login when the server returns 500 Internal Server Error.
    """
    with pytest.raises(HTTPException) as exc_info:
        auth_service_mock.login(potential_user_bytes)
    assert exc_info.value.status_code == 500


def test_auth_service_login_invalid_json(
    auth_service_mock, potential_user_bytes, requests_post_invalid_json
):
    """
    Tests login when the server returns invalid JSON.
    """
    with pytest.raises(ValueError):
        auth_service_mock.login(potential_user_bytes)
