from typing import Dict

from application.services.camera_service import CameraService
from fastapi import APIRouter, Depends

camera_router = APIRouter(prefix="/cameras", tags=["Camera"])

camera_service = CameraService()


def get_camera_service() -> CameraService:
    return camera_service


@camera_router.get("/label")
def get_centroid_and_object_label(
    camera_service: CameraService = Depends(get_camera_service),
) -> Dict:
    """
    Captures a frame from the camera and detects the object's centroid and classification data.

    This endpoint retrieves a frame from the connected camera, processes it to detect an object,
    and returns information including its centroid position, label, prediction confidence,
    and the filename of the captured frame.

    Args:
        camera_service (CameraService): The camera service instance (injected by Depends).

    Returns:
        dict: A dictionary containing the following keys:
            - **cx_global** (float): The x-coordinate of the object's centroid in the global frame.
            - **cy_global** (float): The y-coordinate of the object's centroid in the global frame.
            - **label** (str): The detected object's label.
            - **class_label** (str): The human-readable class name of the object.
            - **prediction** (float): The prediction confidence or probability score.
            - **filename** (str): The name of the saved frame image containing the detection.
    """
    return camera_service.get_centroid_and_label_from_capture_frame()


@camera_router.put("/release-video")
def release_video_capture(
    camera_service: CameraService = Depends(get_camera_service),
) -> bool:
    """
    Releases the current video capture device.

    This endpoint stops the video stream and frees up the camera resource.
    It ensures that the camera connection is properly closed before
    shutting down the application or switching to another process.

    Args:
        camera_service (CameraService): The camera service instance (injected by Depends).

    Returns:
        bool: True if the video capture was successfully released, False otherwise.
    """
    return camera_service.release_video_capture_from_camera()
