import time

from application.entities.real_conveyor_belt import RealConveyorBelt
from application.services.camera_service import CameraService
from application.services.database_service import DatabaseService
from application.services.robot_service import RobotService
from application.utils.mapper import Mapper
from application.utils.storage import Storage


class ConveryorBeltModel:
    # Auto generated code. Please, adjust!
    def __init__(self):
        self.__real_conveyor_belt = RealConveyorBelt()
        self.__real_conveyor_belt.change_speed(600)

        self.__camera_service = CameraService()
        self.__robot_service = RobotService()
        self.__database_service = DatabaseService()

        self.__is_camera_detecting = False
        self.__is_grip_opened = False

        self.__detected_object = {}
        self.__object_color_height_and_category_dict = {
            0: [0.219, "white", "FLAMMABLE"],
            1: [0.242, "green", "RECYCLABLE"],
            2: [0.267, "green", "RECYCLABLE"],
            3: [0.242, "yellow", "RECYCLABLE"],
            4: [0.239, "black", "FLAMMABLE"],
            5: [0.239, "blue", "NON_FLAMMABLE"],
            6: [0.239, "black", "FLAMMABLE"],
            7: [0.241, "yellow", "RECYCLABLE"],
            8: [0.238, "blue", "NON_FLAMMABLE"],
            9: [0.251, "white", "FLAMMABLE"],
        }

    def camera_detects_object(self):
        print("camera_detects_object")

        for _ in range(10):
            detected_object = self.__camera_service.get_centroid_and_object_label()
            if detected_object.get("label") is not None:
                break

        print(detected_object)
        self.__detected_object = detected_object

        user_id = Storage.read_last_user_on_json().get("id", None)
        image = self.__detected_object.get("filename")
        label = self.__detected_object.get("label")
        confidence = self.__detected_object.get("prediction")

        dashboard_dict = Mapper.dashboard_to_dict(user_id, image, label, confidence)

        self.__database_service.register_dashboard(dashboard_dict)

    def go_to_pre_drop_position(self):
        print("go_to_pre_drop_position")
        self.__robot_service.move_robot_to_position_xyz(None, None, 0.3)

    def stop_conveyor_belt(self):
        print("stop_conveyor_belt")
        time.sleep(0.5)
        self.__real_conveyor_belt.stop()
        # self.__real_conveyor_belt.disconnect()

    def activate_gripper(self):
        print("activate_gripper")
        if self.__is_grip_opened:
            self.__robot_service.grab()
            self.__is_grip_opened = False
        else:
            self.__robot_service.release()
            self.__is_grip_opened = True

    def move_robot_to_pre_grasp_position(self):
        print("move_robot_to_pre_grasp_position")
        x = self.__detected_object.get("x")
        y = self.__detected_object.get("y")

        xy_homography = self.__robot_service.get_xy_from_homography_matrix(x, y)

        x_converted = xy_homography.get("x_converted")
        y_converted = xy_homography.get("y_converted")

        self.__robot_service.move_robot_to_position_xyz(x_converted, y_converted, None)

    def select_situation_gripper(self):
        print("select_situation_gripper")
        label = self.__detected_object.get("label")
        if label == 1:
            self.__robot_service.grab()
            self.__is_grip_opened = False
        else:
            self.__robot_service.release()
            self.__is_grip_opened = True

    def move_robot_to_grasp_position(self):
        print("move_robot_to_grasp_position")
        label = self.__detected_object.get("label")
        z = self.__object_color_height_and_category_dict.get(label)[0]
        self.__robot_service.move_robot_to_position_xyz(None, None, z)

    def go_to_safe_position(self):
        print("go_to_safe_position")
        self.__robot_service.move_robot_to_safe_position()

    def orient_gripper_downward(self):
        print("orient_gripper_downward")
        self.__robot_service.orient_gripper_downward()

    def deactivate_gripper(self):
        print("deactivate_gripper")
        if self.__is_grip_opened:
            self.__robot_service.grab()
            self.__is_grip_opened = False
        else:
            self.__robot_service.release()
            self.__is_grip_opened = True

    def start_conveyor_belt(self):
        print("start_conveyor_belt")
        self.__robot_service.move_robot_to_safe_position()
        self.__robot_service.grab()
        self.__real_conveyor_belt.connect()
        self.__real_conveyor_belt.start()

    def go_to_drop_position(self):
        print("go_to_drop_position")
        label = self.__detected_object.get("label")
        self.__robot_service.move_robot_to_drop_position(
            self.__object_color_height_and_category_dict.get(label)[1]
        )

    def reset_state_machine(self):
        print("reset_state_machine")
        self.__is_camera_detecting = False
        self.__is_grip_opened = False
        self.__robot_service.grab()
        self.__real_conveyor_belt.connect()
        self.__real_conveyor_belt.start()
        self.__detected_object = {}

    def camera_detected_object(self):
        print("camera_detected_object")
        predict_data = self.__camera_service.get_centroid_and_object_label()
        label = predict_data["label"]
        if label is not None:
            self.__is_camera_detecting = True
        return self.__is_camera_detecting

    def save_log(self):
        label = self.__detected_object.get("label")

        user_id = Storage.read_last_user_on_json().get("id", None)
        category = self.__object_color_height_and_category_dict.get(label)[2]
        color = self.__object_color_height_and_category_dict.get(label)[1]
        status = "SUCCESS"

        log_dict = Mapper.log_to_dict(user_id, category, color, status)

        self.__database_service.register_log(log_dict)
