from datetime import datetime
from sqlite3 import IntegrityError
from typing import List

from database.dao.log_dao import LogDAO
from database.dao.user_dao import UserDAO
from database.model.log import Log
from database.model.user import User
from database.proto.log import LogList, LogProto, LogRegister, LogResponse
from fastapi import APIRouter, HTTPException, status


class LogService:
    @staticmethod
    def register(log: Log) -> LogResponse:
        """
        Registra um novo log no banco de dados, validando a existência do usuário.

        Args:
            log (Log): Objeto de log contendo informações como user_id, categoria, cor e status.

        Returns:
            LogResponse: Mensagem de confirmação de registro do log.

        Raises:
            HTTPException: 
                - 404 se o usuário não for encontrado.
                - 400 em caso de erro de integridade no banco.
                - 500 para outros erros inesperados.
        """
        try:
            try:
                UserDAO.get_by_id(log.user_id)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User ID {log.user_id} not found.",
                )

            db_log = Log(
                user_id=log.user_id,
                category=log.category,
                color=log.color,
                status=log.status,
                created_at=datetime.now(),
            )

            LogDAO.create(db_log)

            return LogResponse(
                detail=f"Log registered successfully for user {log.user_id}."
            )

        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Database integrity error: {str(e)}",
            )
        except Exception as e:
            import traceback

            traceback.print_exc()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to register log: {str(e)}",
            )

    @staticmethod
    def get_one_by_id_and_created_at(id: int, created_at: datetime) -> LogResponse:
        """
        Busca logs por ID e data de criação.

        Args:
            id (int): ID do log.
            created_at (datetime): Data de criação para filtro.

        Returns:
            LogResponse: Lista de logs encontrados.

        Raises:
            HTTPException:
                - 404 se nenhum log for encontrado.
                - 500 para erros inesperados.
        """
        try:
            db_logs = LogDAO.get_one_by_id_and_created_at(id, created_at)

            if not db_logs:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No logs found for ID {id} at {created_at}'.",
                )
            proto_logs = [
                LogProto(
                    id=db_log.id,
                    user_id=db_log.user_id,
                    category=db_log.category,
                    color=db_log.color,
                    status=db_log.status,
                    created_at=db_log.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    if db_log.created_at
                    else None,
                )
                for db_log in db_logs
            ]

            return LogList(data=proto_logs)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching logs by id: {str(e)}",
            )

    @staticmethod
    def get_all_by_category_and_user_id(user_id: str, category: str) -> LogResponse:
        """
        Retorna todos os logs de um usuário filtrados por categoria.

        Args:
            user_id (str): ID do usuário.
            category (str): Categoria de filtro.

        Returns:
            LogResponse: Lista de logs filtrados.

        Raises:
            HTTPException:
                - 404 se o usuário ou os logs não forem encontrados.
                - 500 em caso de erro interno.
        """
        try:
            try:
                UserDAO.get_by_id(user_id)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User ID {user_id} not found.",
                )
            db_logs = LogDAO.get_all_by_category_and_user_id(user_id, category)

            if not db_logs:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No logs found for user {user_id} in category '{category}'.",
                )
            proto_logs = [
                LogProto(
                    id=db_log.id,
                    user_id=db_log.user_id,
                    category=db_log.category,
                    color=db_log.color,
                    status=db_log.status,
                    created_at=db_log.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    if db_log.created_at
                    else None,
                )
                for db_log in db_logs
            ]

            return LogList(data=proto_logs)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching logs by category: {str(e)}",
            )

    @staticmethod
    def get_all_by_color_and_user_id(user_id: int, color: str) -> LogList:
        """
        Retorna todos os logs de um usuário filtrados por cor.

        Args:
            user_id (int): ID do usuário.
            color (str): Cor do log (ex: 'green', 'red').

        Returns:
            LogList: Lista de logs filtrados pela cor.

        Raises:
            HTTPException:
                - 404 se o usuário ou logs não forem encontrados.
                - 500 em caso de erro inesperado.
        """
        try:
            try:
                UserDAO.get_by_id(user_id)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User ID {user_id} not found.",
                )
            db_logs = LogDAO.get_all_by_color_and_user_id(user_id, color)

            if not db_logs:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No logs found for user {user_id} in category '{color}'.",
                )
            proto_logs = [
                LogProto(
                    id=db_log.id,
                    user_id=db_log.user_id,
                    category=db_log.category,
                    color=db_log.color,
                    status=db_log.status,
                    created_at=db_log.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    if db_log.created_at
                    else None,
                )
                for db_log in db_logs
            ]

            return LogList(data=proto_logs)
        except Exception as e:
            raise HTTPException(detail=f"Error fetching logs by color: {str(e)}")

    @staticmethod
    def get_all_by_status_and_user_id(user_id: int, log_status: str):
        """
            Retorna todos os logs de um usuário filtrados por status.

        Args:
            user_id (int): ID do usuário.
            log_status (str): Status do log (ex: 'success', 'error').

        Returns:
            LogList: Lista de logs com o status especificado.

        Raises:
            HTTPException:
                - 404 se o usuário não for encontrado.
                - 500 em caso de erro inesperado.
        """
        try:
            try:
                UserDAO.get_by_id(user_id)
            except HTTPException:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User ID {user_id} not found.",
                )

            db_logs = LogDAO.get_all_by_status_and_user_id(user_id, log_status)

            if not db_logs:
                return LogList(data=[])

            proto_logs = [
                LogProto(
                    id=lg.id,
                    user_id=lg.user_id,
                    category=lg.category,
                    color=lg.color,
                    status=lg.status,
                    created_at=lg.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    if lg.created_at
                    else None,
                )
                for lg in db_logs
            ]

            return LogList(data=proto_logs)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching logs by status: {str(e)}",
            )

    @staticmethod
    def get_logs_by_user_id(user_id: int) -> LogList:
        """
            Retorna todos os logs associados a um determinado usuário.

        Args:
            user_id (int): ID do usuário.

        Returns:
            LogList: Lista de logs encontrados.

        Raises:
            HTTPException:
                - 404 se o usuário ou logs não forem encontrados.
                - 500 em caso de erro interno.
        """
        try:
            try:
                UserDAO.get_by_id(user_id)
            except FileNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User ID {user_id} not found.",
                )

            db_logs: List[Log] = LogDAO.get_all_by_user_id(user_id)

            if not db_logs:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No logs found for user {user_id}.",
                )

            proto_logs = [
                LogProto(
                    id=db_log.id,
                    category=db_log.category,
                    color=db_log.color,
                    status=db_log.status,
                    created_at=db_log.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                )
                for db_log in db_logs
            ]

            return LogList(data=proto_logs)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}",
            )
        except Exception as e:
            raise FileNotFoundError(f"Log by user_id not found, erro: {e}")

    @staticmethod
    def get_last_execution_by_user_id(user_id: int) -> LogProto:
        """
            Retorna o último log (última execução) de um determinado usuário.

        Args:
            user_id (int): ID do usuário.

        Returns:
            LogProto: Último log registrado pelo usuário.

        Raises:
            HTTPException:
                - 404 se o usuário ou log não forem encontrados.
                - 500 em caso de erro interno.
        """

        try:
            try:
                UserDAO.get_by_id(user_id)
            except FileNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User ID {user_id} not found.",
                )

            db_logs = LogDAO.get_last_execution_by_user_id(user_id)

            if not db_logs:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No logs found for user {user_id} in last execution.",
                )

            proto_logs = [
                LogProto(
                    id=db_logs.id,
                    category=db_logs.category,
                    color=db_logs.color,
                    status=db_logs.status,
                    user_id=db_logs.user_id,
                    created_at=db_logs.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                )
            ]

            return proto_logs

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Unexpected error: {str(e)}",
            )
        except Exception as e:
            raise FileNotFoundError(f"Log by user_id not found, erro: {e}")
