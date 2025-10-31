from datetime import datetime
from database.dao.user_dao import UserDAO
from database.model.user import User

def test_user_dao_create(session, monkeypatch):
    """
    Testa a criação de um novo usuário no banco de dados.

    Verifica se:
        - O usuário recebe um ID após ser criado.
        - Todos os campos (name, username, password) são salvos corretamente.
        - A data de criação (created_at) corresponde ao dia atual.
    """

    monkeypatch.setattr(
        'database.dao.user_dao.get_session',
        lambda: session
    )
    name = 'tester'
    username = 'tester'
    password = 's3nh4'

    new_user = User(
        name=name,
        username=username,
        password=password
    )

    db_user = UserDAO.create(new_user)
    create_date = datetime.now()

    assert db_user.id is not None
    assert db_user.name == name
    assert db_user.username == username
    assert db_user.password == password
    assert db_user.created_at.year == create_date.year
    assert db_user.created_at.month == create_date.month
    assert db_user.created_at.day == create_date.day

def test_get_user_dao_by_username(session, user, monkeypatch):
    """
    Testa a recuperação de um usuário pelo nome de usuário.

    Verifica se:
        - O retorno não é None.
        - Os campos (name, username, password, created_at) correspondem aos valores esperados.
    """

    monkeypatch.setattr(
        'database.dao.user_dao.get_session',
        lambda: session
    )

    db_user = UserDAO.get_user_by_username(user.username)

    assert db_user is not None
    assert db_user.name == user.name
    assert db_user.username == user.username
    assert db_user.password == user.password
    assert db_user.created_at.year == user.created_at.year
    assert db_user.created_at.month == user.created_at.month
    assert db_user.created_at.day == user.created_at.day


def test_user_dao_get_all(session, user):
    """
    Testa a recuperação de todos os usuários do banco de dados.

    Verifica se:
        - O retorno não é None.
        - O retorno é uma lista contendo pelo menos um usuário.
        - Os elementos da lista são instâncias de User.
    """
    
    db_user = UserDAO.get_all()

    assert db_user is not None
    assert isinstance(db_user, list)
    assert len(db_user) > 0
    assert isinstance(db_user[0], User)