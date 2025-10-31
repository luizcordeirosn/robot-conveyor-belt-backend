from typing import List, Optional
from sqlalchemy import delete, select, update, and_
from sqlalchemy.exc import NoResultFound
from database.connection.connection import get_session
from database.model.user import User

class UserDAO:
    
    @staticmethod
    def create(model: User)->User:
        """
            Insere um novo usuário no banco de dados.

        Args:
            model (User): Objeto `User` a ser persistido no banco.

        Returns:
            User: O objeto `User` criado e atualizado com os dados do banco (incluindo o ID gerado).
        """
        
        session = get_session()
        try:
            session.add(model)
            session.commit()
            session.refresh(model)

            return model
        finally:
            session.close()

        
    @staticmethod
    def get_user_by_username(username: str)->Optional[User]:
        """Recupera um usuário com base no nome de usuário (username).

        Args:
            username (str): Nome de usuário a ser buscado.

        Returns:
            Optional[User]: O objeto `User` correspondente, se encontrado.

        Raises:
            NoResultFound: Se nenhum usuário for encontrado com o nome informado.
        """
        session = get_session()

        try:
            #statment
            stmt = select(User).where(User.username == username)

            db_user = session.scalar(stmt)
            if db_user is None:
                raise NoResultFound(f'User {username}, not found.')
            return db_user
        finally: 
            session.close()

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        """Recupera um usuário pelo seu ID.

        Args:
            user_id (int): ID do usuário a ser buscado.

        Returns:
            Optional[User]: O objeto `User` correspondente, se encontrado.

        Raises:
            NoResultFound: Se nenhum usuário for encontrado com o ID informado.
        """
        session = get_session()
        try:
            stmt = select(User).where(User.id == user_id)
            db_user = session.scalar(stmt)
            if db_user is None:
                raise NoResultFound(f'User with ID {user_id} not found.')
            return db_user
        finally:
            session.close()


    
    @staticmethod
    def get_all()->List[User]:
        """Recupera todos os usuários cadastrados no banco de dados.

        Returns:
            List[User]: Lista contendo todos os objetos `User` armazenados.
        """
        session = get_session()

        try:
            stmt = select(User)
            db_user = session.scalars(stmt).all()
            return db_user
        finally:
            session.close()
            
