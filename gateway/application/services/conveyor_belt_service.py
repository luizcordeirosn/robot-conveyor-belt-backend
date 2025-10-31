import threading
import time

from application.entities.converyor_belt_fsm import ConveryorBeltFSM
from application.entities.converyor_belt_model import ConveryorBeltModel
from application.entities.real_conveyor_belt import RealConveyorBelt
from application.services.database_service import DatabaseService
from application.services.robot_service import RobotService
from application.utils.mapper import Mapper
from application.utils.storage import Storage


class ConveyotBeltService:
    def __init__(self):
        self.__real_conveyor_belt = RealConveyorBelt()
        self.__database_service = DatabaseService()
        self.__conveyor_belt_fsm = None
        self.__is_started = False

    def start_conveyor_belt(self):
        """
        Starts the conveyor belt and its FSM loop in a separate thread if not already started.

        Returns:
            bool: True if the conveyor belt started successfully, False if it was already running.
        """
        if self.__conveyor_belt_fsm is None:
            conveyor_belt_model = ConveryorBeltModel()
            self.__conveyor_belt_fsm = ConveryorBeltFSM(conveyor_belt_model)
            self.__is_started = True

            thread = threading.Thread(target=self.__start_loop_conveyor_belt_states)
            thread.start()
        return self.__is_started

    def __start_loop_conveyor_belt_states(self):
        """
        Private method: Loops through the conveyor belt FSM states while the belt is running.
        Handles exceptions by logging errors and resetting the FSM.
        """
        while self.__is_started:
            try:
                self.__conveyor_belt_fsm.next_state()
                time.sleep(0.1)
            except Exception as e:
                print(f"Error in conveyor belt FSM: {e}")

                log_dict = Mapper.log_to_dict(
                    Storage.read_last_user_on_json().get("id")
                )
                self.__database_service.register_log(log_dict)

                self.__reset_conveyor_belt_fsm()

    def stop_conveyor_belt(self):
        """
        Stops the conveyor belt and resets the FSM. Also stops and disconnects
        the real conveyor belt.

        Returns:
            bool: True if the conveyor belt stopped successfully, False otherwise.
        """
        self.__reset_conveyor_belt_fsm()
        self.__real_conveyor_belt.stop()
        self.__real_conveyor_belt.disconnect()

        return not self.__is_started

    def __reset_conveyor_belt_fsm(self):
        """
        Private method: Resets the conveyor belt FSM and marks it as stopped.
        Also closes the robot connection associated with the conveyor belt.
        """
        self.__is_started = False
        self.__conveyor_belt_fsm = None

        conveyor_belt = RobotService()
        conveyor_belt.close_connection_niryo_robot()
