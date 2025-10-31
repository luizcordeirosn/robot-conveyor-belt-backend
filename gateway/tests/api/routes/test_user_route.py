from http import HTTPStatus


def test_post_user_register_success(client, user_route_mock):
    """
    Tests the POST /users endpoint when the UserService returns valid serialized bytes.
    """
    expected_bytes = b"mocked_register_response"
    user_route_mock.register.return_value = expected_bytes

    response = client.post("/users", content=b"mock_register_bytes")

    assert response.status_code == HTTPStatus.OK
    assert response.content == expected_bytes
    assert response.headers["content-type"] == "application/octet-stream"
    user_route_mock.register.assert_called_once_with(b"mock_register_bytes")


def test_post_user_register_failure(client, user_route_mock):
    """
    Tests the POST /users endpoint when the UserService raises an unexpected exception.
    """
    user_route_mock.register.side_effect = Exception("Unexpected error")

    import pytest

    with pytest.raises(Exception, match="Unexpected error"):
        client.post("/users", content=b"mock_register_bytes")
