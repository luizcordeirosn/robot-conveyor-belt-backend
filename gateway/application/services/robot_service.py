from urllib.parse import urlencode

import requests
from dotenv import dotenv_values, find_dotenv

from application.utils.mapper import Mapper
from application.utils.patterns import SingletonMeta


class RobotService(metaclass=SingletonMeta):
    def __init__(self):
        self.__config = dotenv_values(find_dotenv())

    def close_connection_niryo_robot(self):
        """
        Closes the connection with the Niryo robot.

        Returns:
            dict: Response from the robot API indicating success or failure.
        """
        response = requests.put(
            f"{self.__config.get('ROBOT_URL')}/robots/close-connection",
        )

        return Mapper.http_response_to_dict(response)

    def move_robot_to_position_xyz(self, x: int, y: int, z: int):
        """
        Moves the robot to a specified position in 3D space.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.
            z (int): Z coordinate.

        Returns:
            dict: Response from the robot API indicating success or failure.
        """
        params = {
            "x": x,
            "y": y,
            "z": z,
        }

        filtered_params = {
            key: value for key, value in params.items() if value is not None
        }

        base_url = f"{self.__config.get('ROBOT_URL')}/robots/position"
        final_url = base_url

        if filtered_params:
            query_string = urlencode(filtered_params)
            final_url = f"{base_url}?{query_string}"

        response = requests.put(final_url)

        return Mapper.http_response_to_dict(response)

    def move_robot_to_safe_position(self):
        """
        Moves the robot to a predefined safe position.

        Returns:
            dict: Response from the robot API indicating success or failure.
        """
        response = requests.put(
            f"{self.__config.get('ROBOT_URL')}/robots/position/safe",
        )

        return Mapper.http_response_to_dict(response)

    def move_robot_to_drop_position(self, color: str):
        """
        Moves the robot to the drop position for a specific color.

        Args:
            color (str): The color identifier for the drop position.

        Returns:
            dict: Response from the robot API indicating success or failure.
        """
        response = requests.put(
            f"{self.__config.get('ROBOT_URL')}/robots/position/drop?color={color}",
        )

        return Mapper.http_response_to_dict(response)

    def orient_gripper_downward(self):
        """
        Orients the robot's gripper downward.

        Returns:
            dict: Response from the robot API indicating success or failure.
        """
        response = requests.put(
            f"{self.__config.get('ROBOT_URL')}/robots/orientation",
        )

        return Mapper.http_response_to_dict(response)

    def grab(self):
        """
        Commands the robot to grab an object.

        Returns:
            dict: Response from the robot API indicating success or failure.
        """
        response = requests.put(
            f"{self.__config.get('ROBOT_URL')}/robots/grab",
        )

        return Mapper.http_response_to_dict(response)

    def release(self):
        """
        Commands the robot to release an object.

        Returns:
            dict: Response from the robot API indicating success or failure.
        """
        response = requests.put(
            f"{self.__config.get('ROBOT_URL')}/robots/release",
        )

        return Mapper.http_response_to_dict(response)

    def get_xy_from_homography_matrix(self, x, y):
        """
        Converts real-world coordinates to robot workspace coordinates using homography.

        Args:
            x: Real-world X coordinate.
            y: Real-world Y coordinate.

        Returns:
            dict: Dictionary containing converted X and Y coordinates.
        """
        response = requests.get(
            f"{self.__config.get('ROBOT_URL')}/robots/homography?x={x}&y={y}",
        )

        return Mapper.http_response_to_dict(response)
