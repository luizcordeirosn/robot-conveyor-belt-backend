from datetime import datetime

from database.model.log import Log
from database.proto.log import LogList, LogRegister, LogResponse
from database.services.log_service import LogRegister, LogService
from fastapi import APIRouter, HTTPException, status

router_log = APIRouter(
    prefix="/logs",
    tags=["LOG"],
)


@router_log.post("/")
async def register(register: LogRegister):
    """
    Registra um novo log no sistema.

    Args:
        register (LogRegister): Dados do log a serem registrados, incluindo:
            - user_id: ID do usuário
            - category: Categoria do log
            - color: Cor do log
            - status: Status do log

    Returns:
        LogResponse: Mensagem de confirmação do registro.

    Raises:
        HTTPException:
            - 500: Se ocorrer um erro inesperado durante o registro.
    """
    try:
        LogService.register(
            Log(
                user_id=register.user_id,
                category=register.category,
                color=register.color,
                status=register.status,
            )
        )

        return LogResponse(detail="Log registered.")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Process failed when registering a new log.",
        )


@router_log.get("/user/category/{user_id}/{category}")
async def category(user_id: int, category: str):
    """
    Retorna todos os logs de um usuário filtrados por categoria.

    Args:
        user_id (int): ID do usuário.
        category (str): Categoria do log.

    Returns:
        LogList: Lista de logs filtrados pela categoria.

    Raises:
        HTTPException:
            - 500: Se ocorrer um erro inesperado durante a busca.
    """
    try:
        return LogService.get_all_by_category_and_user_id(user_id, category)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@router_log.get("/user/color/{user_id}/{color}")
async def color(user_id: int, color: str):
    """
    Retorna todos os logs de um usuário filtrados por cor.

    Args:
        user_id (int): ID do usuário.
        color (str): Cor do log.

    Returns:
        LogList: Lista de logs filtrados pela cor.

    Raises:
        HTTPException:
            - 500: Se ocorrer um erro inesperado durante a busca.
    """
    try:
        return LogService.get_all_by_color_and_user_id(user_id, color)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@router_log.get("/user/status/{user_id}/{log_status}", response_model=LogList)
async def get_status(user_id: int, log_status: str):
    """
    Retorna todos os logs de um usuário filtrados por status.

    Args:
        user_id (int): ID do usuário.
        log_status (str): Status do log (ex: 'success', 'error').

    Returns:
        LogList: Lista de logs filtrados pelo status.
    """
    return LogService.get_all_by_status_and_user_id(user_id, log_status)


@router_log.get("/user/{user_id}")
async def user(user_id: int):
    """
    Retorna todos os logs associados a um usuário específico.

    Args:
        user_id (int): ID do usuário.

    Returns:
        LogList: Lista de todos os logs do usuário.

    Raises:
        HTTPException:
            - 500: Se ocorrer um erro inesperado durante a busca.
    """
    try:
        return LogService.get_logs_by_user_id(user_id)

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@router_log.get("/user/{user_id}/last-execution/")
def get_last_execution(user_id: int):
    """
    Retorna o último log (última execução) de um usuário.

    Args:
        user_id (int): ID do usuário.

    Returns:
        LogList: Lista contendo apenas o último log do usuário.

    Raises:
        HTTPException:
            - 404: Se o usuário ou log não forem encontrados.
            - 500: Para outros erros inesperados.
    """
    try:
        return LogService.get_last_execution_by_user_id(user_id)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )
