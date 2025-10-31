import cv2
from dotenv import dotenv_values, find_dotenv


class Camera:
    """
    Handles video capture operations using OpenCV.

    This class encapsulates camera initialization, frame capture, and release
    operations. It provides a controlled interface to manage a single
    camera device configured via environment variables.
    """

    def __init__(self):
        self.__video_capture = None
        self.__config = dotenv_values(find_dotenv())

    @property
    def vision_capture(self):
        return self.__video_capture

    def turn_on_video_capture(self):
        """
        Initializes and starts the video capture device.

        Reads the camera number from the `.env` configuration under the key `NUM_CAM`
        and opens the corresponding device using the V4L2 backend.

        Returns:
            bool: True if the video capture was successfully initialized,
            False if it was already active.
        """
        is_turned_on = False
        if self.__video_capture is None:
            self.__video_capture = cv2.VideoCapture(
                int(self.__config.get("NUM_CAM")), cv2.CAP_V4L2
            )
            is_turned_on = True

        return is_turned_on

    def release_video_capture(self):
        """
        Releases the active video capture device.

        This method closes the camera resource and resets the internal
        reference to avoid memory leaks or hardware locks.

        Returns:
            bool: True if the video capture was successfully released,
            False if no active camera was found.
        """
        is_released = False
        if self.__video_capture is not None:
            self.__video_capture.release()
            self.__video_capture = None
            is_released = True

        return is_released

    def capture_current_frame(self):
        """
        Captures a frame from the active video stream.

        Before returning a frame, the method performs a short warm-up by
        discarding the first few frames to ensure the latest image is captured.

        Returns:
            tuple[bool, numpy.ndarray | None]: A tuple containing:
                - success (bool): True if the frame was captured successfully, False otherwise.
                - frame (numpy.ndarray | None): The captured image in BGR format if successful,
                  or None if capture failed or no camera is active.
        """
        if self.__video_capture is None:
            return False, None

        # Warm-up: discard a few initial frames to stabilize the image
        for _ in range(5):
            self.__video_capture.read()

        return self.__video_capture.read()
