import pytest


def test_register_success(user_service_mock, register_bytes):
    result = user_service_mock.register(register_bytes)
    assert result == b"mocked_bytes"


def test_register_error(user_service_post_error, register_bytes):
    with pytest.raises(Exception, match="Connection error"):
        user_service_post_error.register(register_bytes)
