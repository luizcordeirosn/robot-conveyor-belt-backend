import pytest


def test_close_connection_success(robot_service_mock):
    """
    Tests that close_connection_niryo_robot returns a success response
    """
    response = robot_service_mock.close_connection_niryo_robot()
    assert response == {
        "status": "success",
        "message": "Robot connection closed successfully.",
    }


def test_close_connection_error(robot_service_put_error):
    """
    Tests that close_connection_niryo_robot raises an exception when requests.put fails
    """
    with pytest.raises(Exception, match="Connection error"):
        robot_service_put_error.close_connection_niryo_robot()


def test_move_robot_to_position_success(robot_service_mock):
    """
    Tests that move_robot_to_position_xyz returns a success response
    """
    response = robot_service_mock.move_robot_to_position_xyz(1, 2, 3)
    assert response == {
        "status": "success",
        "message": "Robot moved to (1, 2, 3)",
    }


def test_move_robot_to_position_error(robot_service_put_error):
    """
    Tests that move_robot_to_position_xyz raises an exception when requests.put fails
    """
    with pytest.raises(Exception, match="Connection error"):
        robot_service_put_error.move_robot_to_position_xyz(1, 2, 3)


def test_move_robot_to_safe_position_success(robot_service_mock):
    """
    Tests that move_robot_to_safe_position returns a success response
    """
    response = robot_service_mock.move_robot_to_safe_position()
    assert response == {
        "status": "success",
        "message": "Robot moved to safe position.",
    }


def test_move_robot_to_safe_position_error(robot_service_put_error):
    """
    Tests that move_robot_to_safe_position raises an exception when requests.put fails
    """
    with pytest.raises(Exception, match="Connection error"):
        robot_service_put_error.move_robot_to_safe_position()


def test_move_robot_to_drop_position_success(robot_service_mock):
    """
    Tests that move_robot_to_drop_position returns a success response
    """
    response = robot_service_mock.move_robot_to_drop_position("red")
    assert response == {
        "status": "success",
        "message": "Robot moved to drop position for color 'red'.",
    }


def test_move_robot_to_drop_position_error(robot_service_put_error):
    """
    Tests that move_robot_to_drop_position raises an exception when requests.put fails
    """
    with pytest.raises(Exception, match="Connection error"):
        robot_service_put_error.move_robot_to_drop_position("red")


def test_orient_gripper_downward_success(robot_service_mock):
    """
    Tests that orient_gripper_downward returns a success response
    """
    response = robot_service_mock.orient_gripper_downward()
    assert response == {
        "status": "success",
        "message": "Robot gripper oriented downward.",
    }


def test_orient_gripper_downward_error(robot_service_put_error):
    """
    Tests that orient_gripper_downward raises an exception when requests.put fails
    """
    with pytest.raises(Exception, match="Connection error"):
        robot_service_put_error.orient_gripper_downward()


def test_grab_success(robot_service_mock):
    """
    Tests that grab returns a success response
    """
    response = robot_service_mock.grab()
    assert response == {
        "status": "success",
        "message": "Robot gripped the object successfully.",
    }


def test_grab_error(robot_service_put_error):
    """
    Tests that grab raises an exception when requests.put fails
    """
    with pytest.raises(Exception, match="Connection error"):
        robot_service_put_error.grab()


def test_release_success(robot_service_mock):
    """
    Tests that release returns a success response
    """
    response = robot_service_mock.release()
    assert response == {
        "status": "success",
        "message": "Robot released the object successfully.",
    }


def test_release_error(robot_service_put_error):
    """
    Tests that release raises an exception when requests.put fails
    """
    with pytest.raises(Exception, match="Connection error"):
        robot_service_put_error.release()


def test_get_xy_from_homography_matrix_success(robot_service_mock):
    """
    Tests that get_xy_from_homography_matrix returns correct converted XY coordinates
    """
    response = robot_service_mock.get_xy_from_homography_matrix(1, 2)
    assert response == {"x_converted": 1, "y_converted": 2}


def test_get_xy_from_homography_matrix_error(robot_service_get_error):
    """
    Tests that get_xy_from_homography_matrix raises an exception when requests.get fails
    """
    with pytest.raises(Exception, match="Connection error"):
        robot_service_get_error.get_xy_from_homography_matrix(1, 2)
