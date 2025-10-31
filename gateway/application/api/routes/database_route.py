from application.services.database_service import DatabaseService
from fastapi import APIRouter, Response

database_service = DatabaseService()

database_router = APIRouter(prefix="", tags=["Database"])


@database_router.get("/dashboards/user/{user_id}")
def get_dashboards_by_user_id(user_id: int):
    """
    Retrieves all dashboards for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of dashboards associated with the given user ID.
    """
    return database_service.get_dashboards_by_user_id(user_id)


@database_router.get("/logs/user/{user_id}")
def get_logs_by_user_id(user_id: int):
    """
    Retrieves all logs for a specific user as serialized bytes.

    Args:
        user_id (int): The ID of the user.

    Returns:
        Response: HTTP response containing the serialized logs in "application/octet-stream" format.
    """
    logs_by_user_bytes = database_service.get_logs_by_user_id(user_id)
    return Response(content=logs_by_user_bytes, media_type="application/octet-stream")


@database_router.get("/logs/user/{user_id}/last-exec")
def get_log_last_execution_by_user_id(user_id: int):
    """
    Retrieves the last execution log for a specific user as serialized bytes.

    Args:
        user_id (int): The ID of the user.

    Returns:
        Response: HTTP response containing the serialized last execution log in "application/octet-stream" format.
    """
    log_last_execution_by_user_bytes = (
        database_service.get_logs_last_execution_by_user_id(user_id)
    )
    return Response(
        content=log_last_execution_by_user_bytes, media_type="application/octet-stream"
    )
