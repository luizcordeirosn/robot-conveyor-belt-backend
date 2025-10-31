from datetime import datetime
from fastapi import HTTPException,status
from typing import List

from database.model.dashboard import Dashboard
from database.dao.dashboard_dao import DashboardDAO
from database.dao.user_dao import UserDAO
from database.proto.dashboard import DashboardRegister, DashboardProto, DashboardResponse, DashboardList


class DashboardService:

    @staticmethod
    def register(dashboard: Dashboard):
        """Registra um novo dashboard no sistema.

        Valida a existência do usuário antes de registrar o dashboard. 

        Args:
            dashboard (Dashboard): Objeto `Dashboard` contendo os dados a serem registrados.

        Returns:
            DashboardResponse: Mensagem de sucesso indicando que o dashboard foi registrado.

        Raises:
            HTTPException: 
                - 404: Se o usuário informado não existir.
                - 400: Se ocorrer erro de integridade ao salvar o dashboard.
                - 500: Se ocorrer um erro inesperado durante o registro.
        """
        try:
            try:
                UserDAO.get_by_id(dashboard.user_id)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User ID {dashboard.user_id} not found."
                )
            
            db_dashboard =  Dashboard(
                user_id = dashboard.user_id,
                image = dashboard.image,
                label = dashboard.label,
                confidence = dashboard.confidence,
                created_at = datetime.now()
            )
         
            DashboardDAO.create(db_dashboard)  

            return DashboardResponse(detail=f"Dashboard registered successfully.")   
        except HTTPException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error: {str(e)}"
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise HTTPException (
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to register dashboard: {str(e)}"
            )
        

    @staticmethod
    def get_all_by_user_id(user_id: int) -> DashboardList:
        """Recupera todos os dashboards de um usuário específico.

        Valida se o usuário existe antes de realizar a busca.
        Retorna uma lista de dashboards convertida para o formato `DashboardProto`.

        Args:
            user_id (int): ID do usuário cujos dashboards devem ser recuperados.

        Returns:
            DashboardList: Lista contendo os dashboards do usuário.

        Raises:
            HTTPException:
                - 404: Se o usuário ou os dashboards não forem encontrados.
                - 500: Se ocorrer um erro inesperado durante a consulta.
        """
        try:
            try:
                UserDAO.get_by_id(user_id)
            except FileNotFoundError as e:
                raise HTTPException (
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User ID {user_id} not found."
                )
            
            db_dashboards: List[Dashboard] = DashboardDAO.get_all_by_user_id(user_id)

            if not db_dashboards:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No dashboard found for user {user_id}."
                )
            
            proto_dashboards = [
                DashboardProto(
                    id=db_dashboard.id,
                    image=db_dashboard.image,
                    label=db_dashboard.label,
                    confidence=db_dashboard.confidence,
                    user_id=db_dashboard.user_id,
                    created_at=db_dashboard.created_at.strftime('%Y-%m-%d %H:%M:%S')
                )
                for db_dashboard in db_dashboards
            ]

            return DashboardList(data=proto_dashboards)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
        except Exception as e:
            raise FileNotFoundError(f"Dashboard by {user_id} not found, erro: {e}")


    @staticmethod
    def get_all_by_label_and_user_id(user_id: int, label: str) -> DashboardList:
        """Recupera todos os dashboards de um usuário filtrando por um rótulo (label) específico.

        Valida se o usuário existe antes da consulta.
        Retorna uma lista de dashboards no formato `DashboardProto`.

        Args:
            user_id (int): ID do usuário.
            label (str): Rótulo usado para filtrar os dashboards.

        Returns:
            DashboardList: Lista contendo os dashboards filtrados pelo label.

        Raises:
            HTTPException:
                - 404: Se o usuário ou os dashboards com o label informado não forem encontrados.
                - 500: Se ocorrer um erro inesperado durante a consulta.
        """
        try:
            try:
                UserDAO.get_by_id(user_id)
            except FileNotFoundError as e:
                raise HTTPException (
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User ID {user_id} not found."
                )
            
            db_dashboards: List[Dashboard] = DashboardDAO.get_all_by_label_and_user_id(user_id, label)

            if not db_dashboards:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No dashboard found for user {user_id}."
                )
            
            proto_dashboards = [
                DashboardProto(
                    id=db_dashboard.id,
                    image=db_dashboard.image,
                    label=db_dashboard.label,
                    confidence=db_dashboard.confidence,
                    user_id=db_dashboard.user_id,
                    created_at=db_dashboard.created_at.strftime('%Y-%m-%d %H:%M:%S')
                )
                for db_dashboard in db_dashboards
            ]

            return DashboardList(data=proto_dashboards)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}"
            )
        except Exception as e:
            raise FileNotFoundError(f"Label by {user_id} not found, erro: {e}")
        
    