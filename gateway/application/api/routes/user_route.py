from application.services.user_service import UserService
from fastapi import APIRouter, Request, Response

user_service = UserService()

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.post("")
async def register(request: Request):
    """
    Registers a new user.

    Args:
        request (Request): Object containing the request body data (serialized bytes of the user to register).

    Returns:
        Response: HTTP response containing the serialized bytes of the register response in "application/octet-stream" format.
    """
    register_response_bytes = user_service.register(await request.body())
    return Response(
        content=register_response_bytes, media_type="application/octet-stream"
    )
