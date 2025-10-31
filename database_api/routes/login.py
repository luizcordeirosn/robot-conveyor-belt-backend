from database.proto.auth import LoggedUser, PotentialUser
from database.services.user_service import UserService
from fastapi import APIRouter, Depends, HTTPException, status


router_login = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={404: {"description": "Usuário não encontrado"}},
)


@router_login.post("/", status_code=200)
async def login(potential_user: PotentialUser) -> LoggedUser:
    """
        Realiza o login de um usuário com base em suas credenciais.

    Verifica se o nome de usuário existe e se a senha informada é válida.
    Caso as credenciais estejam corretas, retorna os dados básicos do usuário autenticado.

    Args:
        potential_user (PotentialUser): Objeto contendo o nome de usuário e a senha enviados na requisição.

    Returns:
        LoggedUser: Dados do usuário autenticado, incluindo:
            - id (int): Identificador do usuário.
            - name (str): Nome completo.
            - username (str): Nome de usuário.

    Raises:
        HTTPException:
            - 401: Se o nome de usuário ou senha estiver incorreto.
            - 500: Se ocorrer um erro inesperado durante o processo de autenticação.
    """
    try:
        return UserService.get_by_potencial_user(potential_user=potential_user)

    except PermissionError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User unauthorized."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Process failed. {e}"
        )
