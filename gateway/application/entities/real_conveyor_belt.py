import os
import platform
import sys

import serial
import serial.tools.list_ports

sys.path.append(os.path.join(os.path.dirname(__file__)))

from abstract_conveyor_belt import AbstractConveyorBelt
from application.utils.patterns import SingletonMeta


class RealConveyorBelt(AbstractConveyorBelt, metaclass=SingletonMeta):
    def __init__(self):
        self.esp = None
        self.port = None
        self.baudrate = 115200
        self.timeout = 1
        self.connected = False
        self.__actual_direction = 3
        self.__actual_speed = False

    @property
    def get_actual_speed(self):
        """Actual speed of the conveyor."""
        return self.__actual_speed

    @property
    def get_actual_direction(self):
        """Actual direction of the conveyor."""
        if self.__actual_direction == 3:
            return True

        return False

    def connect(self):
        """Method responsible for connecting the system to the Esp."""
        self.__port_detect()
        if not self.port:
            print("No port detected. Please connect the device and try again.")
            return
        try:
            self.esp = serial.Serial(self.port, self.baudrate, timeout=self.timeout)

            self.connected = True
            print(f"Connected to {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"Failed to connect to {self.port}: {e}")
            self.connected = False

    def disconnect(self):
        """Method responsible for disconnecting the system from the Esp."""
        if self.esp and self.connected:
            self.esp.close()
            self.connected = False
            print(f"Disconnected from {self.port}.")
        else:
            print("No connection to close.")

    def is_connected(self):
        """Method responsible for checking if the system is connected."""
        return self.connected

    def start(self):
        """This method starts the conveyor belt moves"""
        if self.connected:
            self.__send_command(2)
        else:
            print("Conveyor not connected")

    def stop(self):
        """This method stops the conveyor belt moves"""
        if self.connected:
            self.__send_command(1)
        else:
            print("Conveyor not connected")

    def change_speed(self, speed: int):
        """Method responsible for changing speed of Esp

        Args:
            speed(int): new speed of Esp this speed is between 5 and 800
        """
        if speed < 5:
            speed = 5

        elif speed > 800:
            speed = 800

        if self.connected:
            self.__send_command(speed)
            self.__actual_speed = speed
        else:
            print("Conveyor not connected")

    def change_direction(self, direction: bool):
        """Method responsible for changing direction of Esp

        Args:
            direction(bool): new direction of conveyor belt if true is
            clockwise false is counterclockwise
        """
        if direction:
            direction = 3
        else:
            direction = 4

        if direction != self.__actual_direction:
            if self.connected:
                self.__send_command(direction)
            else:
                print("Conveyor not connected")

        else:
            print("Conveyor is already in this direction.")

    def __port_detect(self):
        """Method responsible for detecting port for Esp"""
        current_os = platform.system()
        if current_os == "Windows":
            ports = serial.tools.list_ports.comports()
            for port in ports:
                if "Silicon Labs" in port.description:
                    self.port = port.device
        else:
            self.port = "/dev/ttyUSB0"

    def __send_command(self, command):
        """Method responsible for sending command to Esp"""
        if self.connected:
            command = str(command)
            try:
                self.esp.write(command.encode())
            except serial.SerialException as e:
                print(f"Failed to send command: {e}")
        else:
            print("Not connected to any device.")


if __name__ == "__main__":
    comm = RealConveyorBelt()
    comm.connect()
