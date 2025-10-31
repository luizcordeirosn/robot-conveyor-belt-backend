import pytest


def test_register_log(database_service_mock):
    """
    Tests that register_log returns the expected response
    """
    log_dict = {"user_id": 123, "category": "test", "status": "OK"}
    result = database_service_mock.register_log(log_dict)
    assert result == {"detail": "Log registered."}


def test_register_log_error(database_service_post_error):
    """
    Tests that register_log raises an exception when requests.post fails
    """
    with pytest.raises(Exception, match="Connection error"):
        database_service_post_error.register_log({"user_id": 123})


def test_register_dashboard(database_service_mock):
    """
    Tests that register_dashboard returns the expected response
    """
    dashboard_dict = {
        "image": "img.png",
        "label": 5,
        "confidence": 0.95,
        "user_id": 123,
    }
    result = database_service_mock.register_dashboard(dashboard_dict)
    assert result == {"detail": "Dashboard registered successfully."}


def test_register_dashboard_error(database_service_post_error):
    """
    Tests that register_dashboard raises an exception when requests.post fails
    """
    with pytest.raises(Exception, match="Connection error"):
        database_service_post_error.register_dashboard({"image": "img.png"})


def test_get_logs_by_user_id(database_service_mock):
    """
    Tests that get_logs_by_user_id returns serialized log bytes
    """
    result = database_service_mock.get_logs_by_user_id(123)
    assert result == b"mocked_logs_bytes"


def test_get_logs_by_user_id_error(database_service_get_error):
    """
    Tests that get_logs_by_user_id raises an exception when requests.get fails
    """
    with pytest.raises(Exception, match="Connection error"):
        database_service_get_error.get_logs_by_user_id(123)


def test_get_logs_last_execution_by_user_id(database_service_mock):
    """
    Tests that get_logs_last_execution_by_user_id returns serialized last log bytes
    """
    result = database_service_mock.get_logs_last_execution_by_user_id(123)
    assert result == b"mocked_last_log_bytes"


def test_get_logs_last_execution_by_user_id_error(database_service_get_error):
    """
    Tests that get_logs_last_execution_by_user_id raises an exception when requests.get fails
    """
    with pytest.raises(Exception, match="Connection error"):
        database_service_get_error.get_logs_last_execution_by_user_id(123)


def test_get_dashboards_by_user_id(database_service_mock):
    """
    Tests that get_dashboards_by_user_id returns the expected dashboards list
    """
    result = database_service_mock.get_dashboards_by_user_id(123)
    assert result == [
        {"id": 1, "image": "img1.png", "label": 5, "confidence": 0.95, "user_id": 123}
    ]


def test_get_dashboards_by_user_id_error(database_service_get_error):
    """
    Tests that get_dashboards_by_user_id raises an exception when requests.get fails
    """
    with pytest.raises(Exception, match="Connection error"):
        database_service_get_error.get_dashboards_by_user_id(123)
