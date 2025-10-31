from unittest.mock import MagicMock

import pytest
from application.proto.user import PotentialUser, Register
from application.services.auth_service import AuthService
from application.services.camera_service import CameraService
from application.services.conveyor_belt_service import ConveyotBeltService
from application.services.database_service import DatabaseService
from application.services.robot_service import RobotService
from application.services.user_service import UserService
from application.utils.mapper import Mapper
from application.utils.storage import Storage


@pytest.fixture
def potential_user_bytes():
    potential_user = PotentialUser()
    potential_user.username = "john"
    potential_user.password = "1234"
    return potential_user.SerializeToString()


@pytest.fixture
def auth_service_mock(monkeypatch):
    monkeypatch.setattr(
        Mapper,
        "dict_to_logged_user",
        lambda user_dict: MagicMock(SerializeToString=lambda: b"mocked_bytes"),
    )

    monkeypatch.setattr(Storage, "save_last_user_on_json", lambda user_dict: None)

    return AuthService()


@pytest.fixture
def requests_post_success(monkeypatch):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '{"username": "john", "token": "abc123"}'

    monkeypatch.setattr("requests.post", lambda *args, **kwargs: mock_response)
    return mock_response


@pytest.fixture
def requests_post_unauthorized(monkeypatch):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = '{"detail": "Unauthorized"}'

    monkeypatch.setattr("requests.post", lambda *args, **kwargs: mock_response)
    return mock_response


@pytest.fixture
def requests_post_server_error(monkeypatch):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = '{"detail": "Server Error"}'

    monkeypatch.setattr("requests.post", lambda *args, **kwargs: mock_response)
    return mock_response


@pytest.fixture
def requests_post_invalid_json(monkeypatch):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "invalid_json"

    monkeypatch.setattr("requests.post", lambda *args, **kwargs: mock_response)
    return mock_response


@pytest.fixture
def camera_service_mock():
    return CameraService()


@pytest.fixture
def camera_prediction_success_mock(monkeypatch):
    prediction = {
        "x": 0.1,
        "y": 0.2,
        "label": 5,
        "class": "semisphere",
        "confidence": 0.95,
    }
    monkeypatch.setattr(Mapper, "http_response_to_dict", lambda response: prediction)
    return prediction


@pytest.fixture
def camera_prediction_default_mock(monkeypatch):
    default_prediction = {
        "x": 0,
        "y": 0,
        "label": None,
        "class": None,
        "confidence": None,
        "filename": None,
    }
    monkeypatch.setattr(
        Mapper, "http_response_to_dict", lambda response: default_prediction
    )
    return default_prediction


@pytest.fixture
def conveyor_belt_service_mock(monkeypatch):
    mock_database_service = MagicMock()
    monkeypatch.setattr(
        "application.services.conveyor_belt_service.DatabaseService",
        lambda: mock_database_service,
    )
    monkeypatch.setattr(
        "application.services.conveyor_belt_service.RealConveyorBelt", MagicMock()
    )
    monkeypatch.setattr(
        "application.services.conveyor_belt_service.RobotService", MagicMock()
    )
    monkeypatch.setattr(
        Storage,
        "read_last_user_on_json",
        lambda: {"id": 123, "name": "John", "username": "john123"},
    )
    monkeypatch.setattr(
        Mapper,
        "log_to_dict",
        lambda user_id, category="", color="", status="ERROR": {
            "user_id": user_id,
            "category": category,
            "color": color,
            "status": status,
        },
    )
    return ConveyotBeltService()


@pytest.fixture
def robot_service_mock():
    mock_service = MagicMock()
    mock_service.close_connection_niryo_robot.return_value = {
        "status": "success",
        "message": "Robot connection closed successfully.",
    }
    mock_service.move_robot_to_position_xyz.return_value = {
        "status": "success",
        "message": "Robot moved to (1, 2, 3)",
    }
    mock_service.move_robot_to_safe_position.return_value = {
        "status": "success",
        "message": "Robot moved to safe position.",
    }
    mock_service.move_robot_to_drop_position.return_value = {
        "status": "success",
        "message": "Robot moved to drop position for color 'red'.",
    }
    mock_service.orient_gripper_downward.return_value = {
        "status": "success",
        "message": "Robot gripper oriented downward.",
    }
    mock_service.grab.return_value = {
        "status": "success",
        "message": "Robot gripped the object successfully.",
    }
    mock_service.release.return_value = {
        "status": "success",
        "message": "Robot released the object successfully.",
    }
    mock_service.get_xy_from_homography_matrix.return_value = {
        "x_converted": 1,
        "y_converted": 2,
    }
    return mock_service


@pytest.fixture
def robot_service_put_error(monkeypatch):
    monkeypatch.setattr(
        "requests.put",
        lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Connection error")),
    )
    return RobotService()


@pytest.fixture
def robot_service_get_error(monkeypatch):
    monkeypatch.setattr(
        "requests.get",
        lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Connection error")),
    )
    return RobotService()


@pytest.fixture
def database_service_mock(monkeypatch):
    mock_service = MagicMock()
    mock_service.register_log.return_value = {"detail": "Log registered."}
    mock_service.register_dashboard.return_value = {
        "detail": "Dashboard registered successfully."
    }
    mock_service.get_logs_by_user_id.return_value = b"mocked_logs_bytes"
    mock_service.get_logs_last_execution_by_user_id.return_value = (
        b"mocked_last_log_bytes"
    )
    mock_service.get_dashboards_by_user_id.return_value = [
        {"id": 1, "image": "img1.png", "label": 5, "confidence": 0.95, "user_id": 123}
    ]
    return mock_service


@pytest.fixture
def database_service_post_error(monkeypatch):
    monkeypatch.setattr(
        "requests.post",
        lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Connection error")),
    )
    return DatabaseService()


@pytest.fixture
def database_service_get_error(monkeypatch):
    monkeypatch.setattr(
        "requests.get",
        lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Connection error")),
    )
    return DatabaseService()


@pytest.fixture
def register_bytes():
    register = Register()
    register.name = "john"
    register.username = "john"
    register.password = "1234"
    return register.SerializeToString()


@pytest.fixture
def user_service_mock(monkeypatch):
    monkeypatch.setattr(
        Mapper,
        "http_response_to_dict",
        lambda response: {"detail": "User created."},
    )
    monkeypatch.setattr(
        Mapper,
        "dict_to_register_response",
        lambda response: MagicMock(SerializeToString=lambda: b"mocked_bytes"),
    )

    monkeypatch.setattr("requests.post", lambda *args, **kwargs: MagicMock())

    return UserService()


@pytest.fixture
def user_service_post_error(monkeypatch):
    monkeypatch.setattr(
        "requests.post",
        lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Connection error")),
    )
    return UserService()
