from datetime import datetime

from database.dao.dashboard_dao import DashboardDAO
from database.model.dashboard import Dashboard
from database.proto.dashboard import DashboardList, DashboardRegister, DashboardResponse
from database.services.dashboard_service import DashboardService
from fastapi import APIRouter, HTTPException, status

router_dashboard = APIRouter(prefix="/dashboards", tags=["Dashboards"])


@router_dashboard.post("/")
def register_dashboard(register: DashboardRegister):
    """
        Registra um novo dashboard para um usuário.

    Args:
        register (DashboardRegister): Dados do dashboard a serem registrados, incluindo:
            - user_id: ID do usuário dono do dashboard
            - image: URL ou caminho da imagem
            - label: Rótulo do dashboard
            - confidence: Confiança da classificação

    Returns:
        DashboardResponse: Mensagem de sucesso indicando que o dashboard foi registrado.

    Raises:
        HTTPException:
            - 500: Se ocorrer um erro inesperado durante o registro do dashboard.
    """
    try:
        DashboardService.register(
            Dashboard(
                user_id=register.user_id,
                image=register.image,
                label=register.label,
                confidence=register.confidence,
                created_at=datetime.now(),
            )
        )

        return DashboardResponse(detail="Dashboard registered successfully.")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Process failed when registering a new dashboard.",
        )


@router_dashboard.get("/user/{user_id}")
def get_dashboards_by_user_id(user_id: int):
    """
        Recupera todos os dashboards de um usuário específico.

    Args:
        user_id (int): ID do usuário.

    Returns:
        DashboardList: Lista de dashboards do usuário.

    Raises:
        HTTPException:
            - 500: Se ocorrer um erro inesperado durante a busca.
    """
    try:
        return DashboardService.get_all_by_user_id(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


@router_dashboard.get("/label/{user_id}/{label}")
def get_label(user_id: int, label: int):
    """
        Recupera todos os dashboards de um usuário filtrados por label.

    Args:
        user_id (int): ID do usuário.
        label (int): Label pelo qual os dashboards devem ser filtrados.

    Returns:
        DashboardList: Lista de dashboards filtrados pelo label.

    Raises:
        HTTPException:
            - 500: Se ocorrer um erro inesperado durante a busca.
    """
    try:
        return DashboardService.get_all_by_label_and_user_id(user_id, label)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )
