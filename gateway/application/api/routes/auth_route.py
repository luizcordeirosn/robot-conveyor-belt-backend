from application.services.auth_service import AuthService
from fastapi import APIRouter, Request, Response

auth_service = AuthService()

auth_router = APIRouter(prefix="/login", tags=["Authentication"])


@auth_router.post("")
async def login(request: Request):
    """
    Performs user login.

    Args:
        request (Request): Object containing the request body data (bytes of the user to log in).

    Returns:
        Response: HTTP response containing the serialized bytes of the logged-in user, with media_type "application/octet-stream".
    """
    logged_user_bytes = auth_service.login(await request.body())

    return Response(content=logged_user_bytes, media_type="application/octet-stream")
