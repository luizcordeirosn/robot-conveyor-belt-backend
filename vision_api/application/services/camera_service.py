from application.entities.camera import Camera
from application.entities.yolo import Yolo
from application.utils.mapper import Mapper
from application.utils.red_rectangle_detector import RedRectangleDetector


class CameraService:
    def __init__(self):
        self.__camera = Camera()
        self.__yolo = Yolo()
        self.__detector = RedRectangleDetector()

    @property
    def camera(self):
        return self.__camera

    def get_centroid_and_label_from_capture_frame(self):
        """
        Captures a frame from the camera, detects a red rectangular ROI, and performs object classification.

        This method:
            1. Activates the video capture.
            2. Detects red rectangular contours in the current frame.
            3. Defines a region of interest (ROI) based on detected corners.
            4. Crops the ROI and performs YOLO-based object detection.
            5. Computes the object's global centroid coordinates relative to the original frame.
            6. Maps the results into a standardized dictionary structure.

        Returns:
            dict: A dictionary produced by `Mapper.centroid_and_label_to_dict` containing:
                - **cx_global** (float): Global x-coordinate of the detected object's centroid.
                - **cy_global** (float): Global y-coordinate of the detected object's centroid.
                - **label** (str): The object's predicted label (YOLO output).
                - **class_label** (str): Human-readable class name.
                - **prediction** (float): Confidence score of the prediction.
                - **filename** (str): The name of the saved image file with detections.

            If any step fails (e.g., frame not captured, no contours detected, or invalid ROI),
            a default dictionary with `None` or empty values is returned.
        """
        try:
            self.__camera.turn_on_video_capture()
            ret, current_frame = self.camera.capture_current_frame()

            if not ret:
                result = Mapper.centroid_and_label_to_dict()

            # height, width = current_frame.shape[:2]
            # self.__detector.min_contour_area = height * width * 0.001

            # centroids = self.__detector.get_rectangle_centroids(current_frame)
            # if centroids is None or len(centroids) < 4:
            #     result = Mapper.centroid_and_label_to_dict()

            # ordered_points = self.__detector.order_points(current_frame, centroids)
            # if ordered_points is None:
            #     return Mapper.centroid_and_label_to_dict()
            # x_roi = int(ordered_points["top_left"][0])
            # y_roi = int(ordered_points["top_left"][1])
            # x_max = int(ordered_points["bottom_right"][0])
            # y_max = int(ordered_points["bottom_right"][1])

            # 152 121 253 193
            x_roi = 162
            y_roi = 131
            x_max = 385
            y_max = 294

            current_frame_copy = current_frame.copy()
            new_frame = current_frame_copy[y_roi:y_max, x_roi:x_max]
            h_roi, w_roi = new_frame.shape[:2]

            if w_roi == 0 or h_roi == 0:
                result = Mapper.centroid_and_label_to_dict()

            predict = self.__yolo.predict(new_frame)
            if predict is None:
                result = Mapper.centroid_and_label_to_dict()

            label, class_label, prediction, box, filename = predict
            x_local, y_local, _, _ = box.int().tolist()

            cx_global = x_local + x_roi
            cy_global = y_local + y_roi

            print(f"Centroid original: ({cx_global}, {cy_global})")

            result = Mapper.centroid_and_label_to_dict(
                cx_global, cy_global, label, class_label, prediction, filename
            )
        except Exception as e:
            print(f"Error - {e}")
            result = Mapper.centroid_and_label_to_dict()
            print(result)

        return result

    def release_video_capture_from_camera(self):
        """
        Releases the camera device and stops video capture.

        This method ensures that the camera resource is properly closed
        to prevent resource locking or interference with other processes.

        Returns:
            bool: True if the camera was successfully released, False otherwise.
        """
        return self.__camera.release_video_capture()
