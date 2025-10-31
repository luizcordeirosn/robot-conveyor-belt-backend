import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__)))

from abstract_conveyor_belt import AbstractConveyorBelt
from application.utils.patterns import SingletonMeta


class VirtualConveyorBelt(AbstractConveyorBelt, metaclass=SingletonMeta):
    def __init__(self):
        self.connected = False
        self.__actual_direction = True
        self.__actual_speed = False

    @property
    def get_actual_speed(self):
        """Actual speed of the conveyor."""
        return self.__actual_speed

    @property
    def get_actual_direction(self):
        """Actual direction of the conveyor."""
        return self.__actual_direction

    def connect(self):
        """Method responsible for connecting the system to the Esp."""
        if not self.connected:
            self.connected = True
            print("Connected")
        else:
            print("Conveyor is already connected.")

    def disconnect(self):
        """Method responsible for disconnecting the system from the Esp."""
        if self.connected:
            self.connected = False
            print("Disconnected")
        else:
            print("Conveyor is not connected.")

    def is_connected(self):
        """Method responsible for checking if the system is connected."""
        return self.connected

    def start(self):
        """This method starts the conveyor belt moves"""
        if self.connected:
            print("Starting conveyor line to moves")

        else:
            print("Conveyor is not connected.")

    def stop(self):
        """This method stops the conveyor belt moves"""
        if self.connected:
            print("Stop conveyor line to moves")

        else:
            print("Conveyor is not connected.")

    def change_speed(self, speed: int):
        """Method responsible for changing speed of Esp

        Args:
            speed(int): new speed of Esp this speed is between 5 and 800
        """
        if self.connected:
            speed = min(max(speed, 5), 800)

            self.__actual_speed = speed

            print("Speed changed to {}".format(speed))
        else:
            print("Conveyor is not connected.")

    def change_direction(self, direction: bool):
        """Method responsible for changing direction of Esp

        Args:
            direction(bool): new direction of conveyor belt if true is clockwise false is counterclockwise
        """
        if self.connected:
            if direction != self.__actual_direction:
                self.__actual_direction = direction
                print("Change the direction of the conveyor")
            else:
                print("Conveyor is already in this direction.")
        else:
            print("Conveyor is not connected.")
