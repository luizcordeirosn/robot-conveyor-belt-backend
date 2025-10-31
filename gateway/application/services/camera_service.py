import requests
from dotenv import dotenv_values, find_dotenv

from application.utils.mapper import Mapper
from application.utils.patterns import SingletonMeta


class CameraService(metaclass=SingletonMeta):
    def __init__(self):
        self.__config = dotenv_values(find_dotenv())

    def get_centroid_and_object_label(self):
        """
        Retrieves the centroid coordinates and object label detected by the camera.

        Returns:
            dict: A dictionary containing centroid coordinates (x, y), label, class, confidence, etc.
        """
        response = requests.get(f"{self.__config.get('VISION_URL')}/cameras/label")

        return Mapper.http_response_to_dict(response)

    def release_video_capture(self):
        """
        Releases the video capture resource of the camera.

        Returns:
            dict: A dictionary indicating the status of the video capture release operation.
        """
        response = requests.put(
            f"{self.__config.get('VISION_URL')}/cameras/release-video"
        )

        return Mapper.http_response_to_dict(response)
