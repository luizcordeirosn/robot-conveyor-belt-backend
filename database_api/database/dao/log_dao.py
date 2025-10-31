from datetime import datetime
from typing import List, Optional

from database.connection.connection import get_session
from database.model.log import Log
from sqlalchemy import and_, desc, select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError


class LogDAO:
    @staticmethod
    def create(model: Log) -> Log:
        """Insere um novo registro de log no banco de dados.

        Args:
            model (Log): Objeto `Log` a ser persistido.

        Returns:
            Log: O objeto `Log` criado e atualizado com os dados do banco (incluindo o ID gerado).

        Raises:
            SQLAlchemyError: Se ocorrer um erro durante a inserção ou commit da transação.
        """
        session = get_session()
        try:
            session.add(model)
            session.commit()
            session.refresh(model)

            return model
        except SQLAlchemyError as e:
            print(f"Error - {e}")
        finally:
            session.close()

    @staticmethod
    def get_all_by_category_and_user_id(user_id: int, category: str) -> List[Log]:
        """Recupera todos os logs de um usuário filtrando por categoria.

        Args:
            user_id (int): ID do usuário.
            category (str): Categoria usada como filtro (busca case-insensitive).

        Returns:
            List[Log]: Lista de objetos `Log` correspondentes ao filtro.

        Raises:
            NoResultFound: Se nenhum log corresponder à categoria e usuário informados.
        """
        session = get_session()

        try:
            # statment
            stmt = (
                select(Log)
                .where(and_(Log.user_id == user_id, Log.category.ilike(category)))
                .order_by(desc(Log.created_at))
            )

            db_log = session.scalars(stmt).all()
            if db_log is None:
                raise NoResultFound(f"Category {Log.category} not found.")
            return db_log
        finally:
            session.close()

    @staticmethod
    def get_all_by_color_and_user_id(user_id: int, color: str) -> List[Log]:
        """Recupera todos os logs de um usuário filtrando por cor.

        Args:
            user_id (int): ID do usuário.
            color (str): Cor usada como filtro (busca case-insensitive).

        Returns:
            List[Log]: Lista de objetos `Log` correspondentes ao filtro.

        Raises:
            NoResultFound: Se nenhum log corresponder à cor e usuário informados.
        """
        session = get_session()

        try:
            # statment
            stmt = (
                select(Log)
                .where(and_(Log.user_id == user_id, Log.color.ilike(color)))
                .order_by(desc(Log.created_at))
            )

            db_log = session.scalars(stmt).all()
            if db_log is None:
                raise NoResultFound(f"Color {Log.color} not found.")
            return db_log
        finally:
            session.close()

    @staticmethod
    def get_all_by_status_and_user_id(user_id: int, status: str):
        """Recupera todos os logs de um usuário filtrando por status.

        Args:
            user_id (int): ID do usuário.
            status (str): Status usado como filtro (busca case-insensitive).

        Returns:
            List[Log]: Lista de objetos `Log` correspondentes ao filtro.

        Raises:
            NoResultFound: Se nenhum log corresponder ao status e usuário informados.
        """
        session = get_session()

        try:
            # statment
            stmt = (
                select(Log)
                .where(and_(Log.user_id == user_id, Log.status.ilike(status)))
                .order_by(desc(Log.created_at))
            )

            db_log = session.scalars(stmt).all()
            if not db_log:
                raise NoResultFound(f"Status {Log.status} not found.")
            return db_log
        finally:
            session.close()

    @staticmethod
    def get_all_by_user_id(user_id: int) -> List[Log]:
        """Recupera todos os logs associados a um usuário.

        Args:
            user_id (int): ID do usuário.

        Returns:
            List[Log]: Lista de objetos `Log` pertencentes ao usuário.

        Raises:
            NoResultFound: Se nenhum log for encontrado para o usuário informado.
        """
        session = get_session()

        try:
            # statment
            stmt = (
                select(Log).where(Log.user_id == user_id).order_by(desc(Log.created_at))
            )

            db_log = session.scalars(stmt).all()
            if db_log is None:
                raise NoResultFound(f"Color {Log.color} not found.")
            return db_log
        finally:
            session.close()

    @staticmethod
    def get_last_execution_by_user_id(user_id: int) -> Optional[Log]:
        """Recupera o último log registrado por um usuário.

        Args:
            user_id (int): ID do usuário.

        Returns:
            Optional[Log]: O último registro de log encontrado ou `None` se não houver registros.

        Raises:
            NoResultFound: Se nenhum log for encontrado para o usuário informado.
        """
        session = get_session()

        try:
            stmt = (
                select(Log)
                .where(Log.user_id == user_id)
                .order_by(desc(Log.id), desc(Log.created_at))
                .limit(1)
            )

            db_log = session.scalar(stmt)

            if db_log is None:
                raise NoResultFound(
                    f"Last execution for this user {Log.user_id} not found."
                )
            return db_log

        finally:
            session.close()
