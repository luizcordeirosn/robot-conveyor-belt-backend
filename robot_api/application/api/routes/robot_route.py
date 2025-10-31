from fastapi import APIRouter, HTTPException

from application.services.robot_service import RobotService

robot_router = APIRouter(prefix="/robots", tags=["Robot Routes"])

robot_service = RobotService()


@robot_router.put("/close-connection")
def close_connection_niryo_robot():
    """
    Closes the connection to the Niryo robot.

    Returns:
        dict: A dictionary with the status and message of the operation.
    """
    success = robot_service.close_connection_niryo_robot()
    if success:
        return {
            "status": "success",
            "message": "Robot connection closed successfully.",
        }
    return {
        "status": "info",
        "message": "Robot connection was not open or already closed.",
    }


@robot_router.put("/position")
def move_robot_to_position_xyz(x: float = None, y: float = None, z: float = None):
    """
    Moves the robot to the specified XYZ position.

    Args:
        x (float, optional): X coordinate.
        y (float, optional): Y coordinate.
        z (float, optional): Z coordinate.

    Raises:
        HTTPException: If an unexpected error occurs during movement.

    Returns:
        dict: A dictionary with the status and message of the operation.
    """
    try:
        success = robot_service.move_robot_to_position_xyz(x, y, z)
        if success:
            return {"status": "success", "message": f"Robot moved to ({x}, {y}, {z})"}
    except Exception as e:
        robot_service.close_connection_niryo_robot()
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


@robot_router.put("/position/safe")
def move_robot_to_safe_position():
    """
    Moves the robot to a predefined safe position.

    Returns:
        dict: A dictionary with the status and message of the operation.
    """
    robot_service.move_robot_to_safe_position()
    return {"status": "success", "message": "Robot moved to safe position."}


@robot_router.put("/position/drop")
def move_robot_to_drop_position(color: str):
    """
    Moves the robot to a drop position for the specified color.

    Args:
        color (str): The color for which the drop position is set.

    Raises:
        HTTPException: If an invalid color or unexpected error occurs.

    Returns:
        dict: A dictionary with the status and message of the operation.
    """
    try:
        robot_service.move_robot_to_drop_position(color)
        return {
            "status": "success",
            "message": f"Robot moved to drop position for color '{color}'.",
        }
    except ValueError as e:
        robot_service.close_connection_niryo_robot()
        raise HTTPException(status_code=400, detail=str(e))


@robot_router.put("/orientation")
def orient_gripper_downward():
    """
    Orients the robot gripper downward.

    Raises:
        HTTPException: If an unexpected error occurs.

    Returns:
        dict: A dictionary with the status and message of the operation.
    """
    try:
        success = robot_service.orient_gripper_downward()
        if success:
            return {
                "status": "success",
                "message": "Robot gripper oriented downward.",
            }
    except Exception as e:
        robot_service.close_connection_niryo_robot()
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


@robot_router.put("/grab")
def grab():
    """
    Commands the robot to grab an object.

    Raises:
        HTTPException: If an unexpected error occurs.

    Returns:
        dict: A dictionary with the status and message of the operation.
    """
    try:
        robot_service.grab()
        return {
            "status": "success",
            "message": "Robot gripped the object successfully.",
        }
    except Exception as e:
        robot_service.close_connection_niryo_robot()
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


@robot_router.put("/release")
def release():
    """
    Commands the robot to release an object.

    Raises:
        HTTPException: If an unexpected error occurs.

    Returns:
        dict: A dictionary with the status and message of the operation.
    """
    try:
        robot_service.release()
        return {
            "status": "success",
            "message": "Robot released the object successfully.",
        }
    except Exception as e:
        robot_service.close_connection_niryo_robot()
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


@robot_router.get("/homography")
def get_xy_from_homography_matrix(x: int, y: int):
    """
    Converts XY coordinates using the robot's homography matrix.

    Args:
        x (int): X coordinate.
        y (int): Y coordinate.

    Raises:
        HTTPException: If an unexpected error occurs during conversion.

    Returns:
        dict: A dictionary containing the converted XY coordinates.
    """
    try:
        return robot_service.get_xy_from_homography_matrix(x, y)
    except Exception as e:
        robot_service.close_connection_niryo_robot()
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )
