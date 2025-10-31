import os
from datetime import datetime

from dotenv import dotenv_values, find_dotenv
from ultralytics import YOLO


class Yolo:
    """
    Handles object detection using a pre-trained YOLO model.

    This class wraps the Ultralytics YOLO interface to simplify
    model loading, inference, and result processing, returning
    structured data that can be consumed by other services.
    """

    def __init__(self):
        self.__model_path = dotenv_values(find_dotenv()).get("WEIGHTS_PATH")
        self.__model = self.load_model()

    def load_model(self):
        """
        Loads the YOLO model from the configured path.

        Returns:
            ultralytics.YOLO: The initialized YOLO model.
        """
        return YOLO(self.__model_path)

    def predict(self, image):
        """
        Runs object detection on the provided image.

        Performs inference using the YOLO model with a confidence
        threshold of 0.80. If objects are detected, it extracts
        the predicted class, confidence, bounding box coordinates,
        and saves the annotated image to disk.

        Args:
            image (numpy.ndarray): The image (in BGR or RGB format)
                on which the detection will be performed.

        Returns:
            tuple[int, str, float, numpy.ndarray, str] | None:
                A tuple containing:
                    - label (int): The predicted class index.
                    - name_class_predicted (str): The name of the predicted class.
                    - confidence (float): The model's confidence score (0.0–1.0).
                    - xywh (numpy.ndarray): The bounding box [x, y, w, h].
                    - filename (str): The name of the saved image file.

                Returns None if no object is detected.
        """
        result = self.__model.predict(image, conf=0.80)

        cls_predicted = result[0].boxes.cls
        if len(cls_predicted) == 0:
            return None

        label = cls_predicted[0].item()
        name_class_predicted = result[0].names.get(label)
        confidence = result[0].boxes.conf[0].item()
        xywh = result[0].boxes.xywh[0]

        os.makedirs("images", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{label}-image-{timestamp}.jpg"
        result[0].save(filename=f"images/{filename}")

        return label, name_class_predicted, confidence, xywh, filename
