from http import HTTPStatus

import pytest


def test_get_dashboards_by_user(client, database_route_mock):
    """
    Tests the GET /dashboards/user/{user_id} endpoint when the DatabaseService
    returns a valid dashboard dictionary for the specified user.
    """
    database_route_mock.get_dashboards_by_user_id.return_value = {
        "dashboards": [1, 2, 3]
    }

    response = client.get("/dashboards/user/42")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"dashboards": [1, 2, 3]}


def test_get_dashboards_by_user_failure(client, database_route_mock):
    """
    Tests the GET /dashboards/user/{user_id} endpoint when the DatabaseService
    raises an exception.
    """
    database_route_mock.get_dashboards_by_user_id.side_effect = Exception(
        "Unexpected error"
    )

    with pytest.raises(Exception, match="Unexpected error"):
        client.get("/dashboards/user/42")


def test_get_logs_by_user_id(client, database_route_mock):
    """
    Tests the GET /logs/user/{user_id} endpoint when the DatabaseService
    returns serialized log bytes for the specified user.
    """
    expected_bytes = b"mocked_logs_bytes"
    database_route_mock.get_logs_by_user_id.return_value = expected_bytes

    response = client.get("/logs/user/42")

    assert response.status_code == HTTPStatus.OK
    assert response.content == expected_bytes
    assert response.headers["content-type"] == "application/octet-stream"


def test_get_logs_by_user_id_failure(client, database_route_mock):
    """
    Tests the GET /logs/user/{user_id} endpoint when the DatabaseService
    raises an exception.
    """
    database_route_mock.get_logs_by_user_id.side_effect = Exception("Unexpected error")

    with pytest.raises(Exception, match="Unexpected error"):
        client.get("/logs/user/42")


def test_get_log_last_execution_by_user_id(client, database_route_mock):
    """
    Tests the GET /logs/user/{user_id}/last-exec endpoint when the DatabaseService
    returns serialized bytes of the last execution log for the specified user.
    """
    expected_bytes = b"mocked_last_exec_bytes"
    database_route_mock.get_logs_last_execution_by_user_id.return_value = expected_bytes

    response = client.get("/logs/user/42/last-exec")

    assert response.status_code == HTTPStatus.OK
    assert response.content == expected_bytes
    assert response.headers["content-type"] == "application/octet-stream"


def test_get_log_last_execution_by_user_id_failure(client, database_route_mock):
    """
    Tests the GET /logs/user/{user_id}/last-exec endpoint when the DatabaseService
    raises an exception.
    """
    database_route_mock.get_logs_last_execution_by_user_id.side_effect = Exception(
        "Unexpected error"
    )

    with pytest.raises(Exception, match="Unexpected error"):
        client.get("/logs/user/42/last-exec")
