from application.services.conveyor_belt_service import ConveyotBeltService
from fastapi import APIRouter

conveyor_belt_service = ConveyotBeltService()

conveyor_belt_router = APIRouter(prefix="/conveyor-belt", tags=["Conveyor Belt"])


@conveyor_belt_router.put("/start")
def start_conveyor_belt():
    """
    Starts the conveyor belt.

    Returns:
        bool: True if the conveyor belt started successfully, False otherwise.
    """
    return conveyor_belt_service.start_conveyor_belt()


@conveyor_belt_router.put("/stop")
def stop_conveyor_belt():
    """
    Stops the conveyor belt.

    Returns:
        bool: True if the conveyor belt stopped successfully, False otherwise.
    """
    return conveyor_belt_service.stop_conveyor_belt()
