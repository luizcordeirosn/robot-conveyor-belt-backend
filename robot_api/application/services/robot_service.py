import json

import numpy as np
from dotenv import dotenv_values, find_dotenv

from application.entities.robot import Robot
from application.utils.parttners import Singleton


class RobotService(Singleton):
    def __init__(self):
        self.__niryo_robot = None
        self.__config = dotenv_values(find_dotenv())

    def init_connection_niryo_robot(self):
        """
        Initializes the connection to the Niryo robot if not already connected.
        """
        if self.__niryo_robot is None:
            self.__niryo_robot = Robot(self.__config.get("NIRYO_ROBOT_IP"))

    def close_connection_niryo_robot(self):
        """
        Closes the connection to the Niryo robot if it is open.

        Returns:
            bool: True if the connection was closed, False if it was already closed.
        """
        is_closed = False

        if self.__niryo_robot is not None:
            self.__niryo_robot.close_connection()
            self.__niryo_robot = None

            is_closed = True

        return is_closed

    def move_robot_to_safe_position(self):
        """
        Moves the robot to a predefined safe position.

        Returns:
            bool: True if the operation was successful.
        """
        print("Moving robot to safe position...")
        self.init_connection_niryo_robot()
        self.__niryo_robot.move_robot_to_safe_position_by_cartesian()

        return True

    def move_robot_to_position_xyz(self, x, y, z):
        """
        Moves the robot to the specified XYZ coordinates.

        Args:
            x (float): X coordinate.
            y (float): Y coordinate.
            z (float): Z coordinate.

        Returns:
            bool: True if the operation was successful.
        """
        print(f"Moving robot to position ({x}, {y}, {z})...")
        self.init_connection_niryo_robot()
        self.__niryo_robot.move_robot_to_position_xyz(x, y, z)

        return True

    def move_robot_to_drop_position(self, color):
        """
        Moves the robot to a predefined drop position based on color.

        Args:
            color (str): The color determining the drop position.

        Raises:
            ValueError: If the color is unknown.

        Returns:
            bool: True if the operation was successful.
        """
        color = color.lower()

        if color == "black" or color == "white":
            position_name = "FLAMMABLE_POSITION"
        elif color == "blue":
            position_name = "NON_FLAMMABLE_POSITION"
        elif color == "green" or color == "yellow":
            position_name = "RECYCLABLE_POSITION"
        else:
            raise ValueError(f"Unknown color: {color}")

        print(f"Moving robot to drop position '{position_name}'...")
        self.init_connection_niryo_robot()
        self.__niryo_robot.move_robot_to_drop_position(position_name)

        return True

    def orient_gripper_downward(self):
        """
        Orients the robot gripper downward.

        Returns:
            bool: True if the operation was successful.
        """
        print("Orienting gripper downward...")
        self.init_connection_niryo_robot()
        self.__niryo_robot.orient_gripper_downward()

        return True

    def grab(self):
        """
        Commands the robot to grab an object.

        Returns:
            bool: True if the operation was successful.
        """
        print("Robot is grabbing the object...")
        self.init_connection_niryo_robot()
        self.__niryo_robot.grab()

        return True

    def release(self):
        """
        Commands the robot to release an object.

        Returns:
            bool: True if the operation was successful.
        """
        print("Robot is releasing the object...")
        self.init_connection_niryo_robot()
        self.__niryo_robot.release()

        return True

    def get_xy_from_homography_matrix(self, x, y):
        """
        Converts XY coordinates using a homography matrix loaded from a JSON file.

        Args:
            x (float): X coordinate in the image.
            y (float): Y coordinate in the image.

        Returns:
            dict: A dictionary containing converted coordinates: {"x_converted": float, "y_converted": float}.
        """
        with open("assets/homography.json", "r+") as file:
            homography_matrix = json.load(file)

            dot_image = np.array([[x, y, 1]], dtype=np.float32).T
            coordinates = np.dot(homography_matrix, dot_image)

            x = float((coordinates[0] / coordinates[2])[0])
            y = float((coordinates[1] / coordinates[2])[0])

            return {"x_converted": x, "y_converted": y}
