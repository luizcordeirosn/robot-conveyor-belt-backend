from typing import List, Optional

from database.connection.connection import get_session
from database.model.dashboard import Dashboard
from sqlalchemy import and_, select, desc
from sqlalchemy.exc import NoResultFound, SQLAlchemyError


class DashboardDAO:
    @staticmethod
    def create(model: Dashboard) -> Dashboard:
        """Insere um novo registro de dashboard no banco de dados.

        Args:
            model (Dashboard): Objeto `Dashboard` a ser persistido.

        Returns:
            Dashboard: O objeto `Dashboard` criado e atualizado com os dados do banco (incluindo ID gerado).

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
    def get_all_by_user_id(user_id: int) -> List[Dashboard]:
        """Recupera todos os dashboards associados a um usuário específico.

        Args:
            user_id (int): ID do usuário para o qual os dashboards serão buscados.

        Returns:
            List[Dashboard]: Lista de objetos `Dashboard` pertencentes ao usuário.

        Raises:
            NoResultFound: Se nenhum dashboard for encontrado para o usuário informado.
        """
        session = get_session()

        try:
            # statment
            stmt = (
                select(Dashboard)
                .where(Dashboard.user_id == user_id)
                .order_by(desc(Dashboard.created_at))
            )

            db_dashboard = session.scalars(stmt).all()
            if db_dashboard is None:
                raise NoResultFound(
                    f"Image {Dashboard.image} with {Dashboard.user_id} not found."
                )
            return db_dashboard
        finally:
            session.close()

    @staticmethod
    def get_all_by_label_and_user_id(user_id: int, label: int) -> List[Dashboard]:
        """Recupera todos os dashboards de um usuário com base em um rótulo (label) específico.

        Args:
            user_id (int): ID do usuário para o qual os dashboards serão buscados.
            label (int): Rótulo (label) usado para filtrar os dashboards.

        Returns:
            List[Dashboard]: Lista de objetos `Dashboard` correspondentes ao filtro informado.

        Raises:
            NoResultFound: Se nenhum dashboard corresponder ao rótulo e usuário informados.
        """
        session = get_session()

        try:
            # statment
            stmt = (
                select(Dashboard)
                .where(and_(Dashboard.user_id == user_id, Dashboard.label == label))
                .order_by(desc(Dashboard.created_at))
            )

            db_dashboard = session.scalars(stmt).all()
            if db_dashboard is None:
                raise NoResultFound(f"Label {Dashboard.label} not found.")
            return db_dashboard
        finally:
            session.close()
