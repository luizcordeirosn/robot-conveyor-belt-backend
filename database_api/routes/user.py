from database.model.user import User
from database.proto.auth import Register, RegisterResponse
from database.services.user_service import UserService
from fastapi import APIRouter, HTTPException, status

router_user = APIRouter(
    prefix="/users",
    tags=["USER"],
)


@router_user.post("/")
async def register(register: Register):
    """
         Registra um novo usuário no sistema.

    Este endpoint cria um novo usuário com nome, nome de usuário e senha.
    A senha é automaticamente criptografada antes de ser salva no banco de dados.

    Args:
        register (Register): Objeto contendo as informações do usuário:
            - name (str): Nome completo do usuário.
            - username (str): Nome de usuário (único).
            - password (str): Senha em texto puro, que será criptografada.

    Returns:
        RegisterResponse: Mensagem de sucesso confirmando a criação do usuário.

    Raises:
        HTTPException:
            - 500: Se ocorrer um erro inesperado durante o processo de registro.
    """
    try:
        UserService.register(
            User(
                name=register.name,
                username=register.username.lower(),
                password=register.password,
            )
        )

        return RegisterResponse(detail="User created.")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Process failed when are creating a new user",
        )
