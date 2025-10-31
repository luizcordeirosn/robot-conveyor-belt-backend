from pyniryo import NiryoRobot


class Robot:
    """
    Represents a Niryo robot with pre-defined positions and methods to control its movement and gripper.

    Attributes:
        POSITIONS (dict): Pre-defined joint positions for safe catching, flammable, non-flammable, and recyclable objects.
    """

    POSITIONS = {
        "SAFE_CATCH_POSITION": [-0.02, 0.60, -0.34, 0, -1.48, -0.04],
        "FLAMMABLE_POSITION": [0.180, 0.321, 0.257, -0.233, 1.489, 1.075],
        "NON_FLAMMABLE_POSITION": [0.070, 0.361, 0.257, -0.393, 1.547, 1.221],
        "RECYCLABLE_POSITION": [-0.043, 0.330, 0.238, -0.741, 1.439, 1.325],
    }

    def __init__(self, ip):
        self.__ip = ip
        self.__connection = NiryoRobot(ip_address=ip)

        self.__connection.calibrate_auto()

    @property
    def ip(self):
        return self.__ip

    @property
    def connection(self):
        return self.__connection

    def close_connection(self):
        """Closes the connection to the Niryo robot."""
        self.__connection.close_connection()

    def move_robot_to_safe_position_by_cartesian(self):
        """
        Moves the robot to the predefined safe catch position using joint coordinates.
        """
        safe_catch_position = Robot.POSITIONS["SAFE_CATCH_POSITION"]

        self.__connection.move_joints(safe_catch_position)

    def move_robot_to_position_xyz(self, x, y, z):
        """
        Moves the robot to specified XYZ coordinates while keeping its current orientation.

        Args:
            x (float): X coordinate (optional, uses current if None).
            y (float): Y coordinate (optional, uses current if None).
            z (float): Z coordinate (optional, uses current if None).
        """
        current_pose = self.__connection.get_pose()

        x = x if x is not None else current_pose.x
        y = y if y is not None else current_pose.y
        z = z if z is not None else current_pose.z

        new_pose = [x, y, z, current_pose.roll, current_pose.pitch, current_pose.yaw]

        self.__connection.move_pose(new_pose)

    def move_robot_to_drop_position(self, position_name):
        """
        Moves the robot to a predefined drop position based on the position name.

        Args:
            position_name (str): The name of the drop position (e.g., 'FLAMMABLE_POSITION').
        """
        drop_position = Robot.POSITIONS.get(position_name)

        self.__connection.move_pose(drop_position)

    def orient_gripper_downward(self):
        """
        Orients the robot's gripper downward by adjusting roll and pitch.
        """
        current_pose = self.__connection.get_pose()
        current_pose.roll = 0.0
        current_pose.pitch = 1.527
        # current_pose.yaw = 0.0

        self.__connection.move_pose(current_pose)

    def grab(self):
        """Closes the robot's gripper to grab an object."""
        self.__connection.close_gripper()

    def release(self):
        """Opens the robot's gripper to release an object."""
        self.__connection.open_gripper()
