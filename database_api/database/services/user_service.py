import bcrypt
from database.dao.user_dao import UserDAO
from database.model.user import User
from database.proto.auth import LoggedUser, PotentialUser
from sqlalchemy.exc import NoResultFound

class UserService:
    @staticmethod
    def register(user: User):
        """
            Registra um novo usuário no sistema com a senha criptografada.

        Args:
            user (User): Objeto contendo as informações do usuário a ser registrado.

        Returns:
            None

        Raises:
            Exception: Caso ocorra erro durante a criação do usuário no banco.
        """
        salt = bcrypt.gensalt(12)
        hash_password = bcrypt.hashpw(user.password.encode("utf-8"), salt)
        user.password = hash_password

        UserDAO.create(user)

    @staticmethod
    def get_by_potencial_user(potential_user: PotentialUser): 
        """
            Autentica um usuário com base nas credenciais fornecidas.

        Args:
            potential_user (PotentialUser): Objeto contendo `username` e `password` do usuário.

        Returns:
            LoggedUser: Objeto contendo informações do usuário autenticado (id, nome e username).

        Raises:
            PermissionError:
                - Se o usuário não existir.
                - Se a senha estiver incorreta.
        """ 
        try:
            user = UserDAO.get_user_by_username(potential_user.username)
        except NoResultFound:
           raise PermissionError("User unauthorized.")
        
        stored_pass = user.password.encode("utf-8")
        plain_password = potential_user.password.encode("utf-8")

        if isinstance(stored_pass, str):
            stored_pass = stored_pass.encode("utf-8")

        if not bcrypt.checkpw(plain_password, stored_pass):
            raise PermissionError("Password doesn't match")

        return LoggedUser(id=user.id, name=user.name, username=user.username)
