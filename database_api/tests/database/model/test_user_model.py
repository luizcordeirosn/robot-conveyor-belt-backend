
from sqlalchemy import select

from database.model.user import User


def test_user_model_creation(session):
    """
    Testa a criação de uma instância do modelo User.

    Verifica se:
        - O nome da tabela do modelo é 'users'.
        - Os campos (name, username, password) são atribuídos corretamente.
        - O ID é gerado como um inteiro após adicionar e commitar no banco de dados.
    """

    assert User.__tablename__ == 'users'

    new_user = User(
        name='test',
        username='testuser',
        password='test123',
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    assert isinstance(new_user.id, int)
    assert new_user.name == 'test'
    assert new_user.username == 'testuser'
    assert new_user.password == 'test123'
    

def test_user_model_selected(session, user):
    """
    Testa a recuperação de uma instância de User do banco de dados.

    Verifica se:
        - O usuário recuperado não é None.
        - Os campos (name, username, password) correspondem aos valores esperados.
        - A data de criação (created_at) está presente e é consistente com o usuário original.
    """

    db_user = session.scalar(
        select(User).where(User.id == user.id)
    )

    assert db_user is not None
    assert db_user.name == user.name
    assert db_user.username == user.username
    assert db_user.password == user.password
    assert db_user.created_at == user.created_at

def test_user_model_as_dict(user):
    """
    Testa o método `as_dict()` do modelo User.

    Verifica se:
        - O retorno é um dicionário.
        - Todas as chaves ('id', 'name', 'username', 'password', 'created_at') existem.
        - Os valores do dicionário correspondem aos atributos do usuário.
    """
    user_dict = user.as_dict()

    assert isinstance(user_dict, dict)
    assert user_dict['id'] == user.id
    assert user_dict['name'] == user.name
    assert user_dict['username'] == user.username
    assert user_dict['password'] == user.password
    assert user_dict['created_at'] == user.created_at