def test_close_connection_success(client, robot_service_mock):
    """
    Test the PUT /robots/close-connection route when the robot connection
    is successfully closed.
    """
    robot_service_mock.close_connection_niryo_robot.return_value = True

    response = client.put("/robots/close-connection")

    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Robot connection closed successfully.",
    }


def test_close_connection_not_open(client, robot_service_mock):
    """
    Test the PUT /robots/close-connection route when the connection
    was not open or already closed.
    """
    robot_service_mock.close_connection_niryo_robot.return_value = False

    response = client.put("/robots/close-connection")

    assert response.status_code == 200
    assert response.json()["status"] == "info"


def test_move_robot_to_position_xyz_success(client, robot_service_mock):
    """
    Test the PUT /robots/position route when the robot successfully moves
    to a specific (x, y, z) position.
    """
    robot_service_mock.move_robot_to_position_xyz.return_value = True

    response = client.put("/robots/position", params={"x": 1.0, "y": 2.0, "z": 3.0})

    assert response.status_code == 200
    assert "success" in response.json()["status"]


def test_move_robot_to_drop_position_invalid_color(client, robot_service_mock):
    """
    Test the PUT /robots/position/drop route when an invalid color
    is provided, raising a ValueError.
    """
    robot_service_mock.move_robot_to_drop_position.side_effect = ValueError(
        "Unknown color"
    )

    response = client.put("/robots/position/drop", params={"color": "pink"})

    assert response.status_code == 400
    assert "Unknown color" in response.json()["detail"]


def test_move_robot_to_safe_position(client, robot_service_mock):
    """
    Test the PUT /robots/position/safe route when the robot moves
    to the predefined safe position.
    """
    response = client.put("/robots/position/safe")

    assert response.status_code == 200
    assert response.json()["message"] == "Robot moved to safe position."


def test_orient_gripper_downward_success(client, robot_service_mock):
    """
    Test the PUT /robots/orientation route when the robot successfully
    orients its gripper downward.
    """
    robot_service_mock.orient_gripper_downward.return_value = True

    response = client.put("/robots/orientation")

    assert response.status_code == 200
    assert "Robot gripper oriented downward." in response.json()["message"]


def test_grab_success(client, robot_service_mock):
    """
    Test the PUT /robots/grab route when the robot successfully grabs an object.
    """
    response = client.put("/robots/grab")

    assert response.status_code == 200
    assert "Robot gripped" in response.json()["message"]


def test_release_success(client, robot_service_mock):
    """
    Test the PUT /robots/release route when the robot successfully releases an object.
    """
    response = client.put("/robots/release")

    assert response.status_code == 200
    assert "Robot released" in response.json()["message"]
