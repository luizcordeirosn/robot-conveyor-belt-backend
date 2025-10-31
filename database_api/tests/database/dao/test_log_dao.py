from datetime import datetime
from database.dao.log_dao import LogDAO
from database.model.log import Log

def test_log_dao_create(session, monkeypatch):
    """
    Testa a criação de um novo log no banco de dados.

    Verifica se:
        - Os campos category, color, status e user_id são salvos corretamente.
        - A data de criação (created_at) corresponde ao dia atual.
    """

    monkeypatch.setattr(
        'database.dao.log_dao.get_session',
        lambda: session
    )

    category='reciclável'
    color='verde'
    status='OK'
    user_id=1

    new_log = Log(
        category=category,
        color=color,
        status=status,
        user_id=user_id
    )

    db_log = LogDAO.create(new_log)
    create_date = datetime.now()

    assert db_log.category == category
    assert db_log.color == color
    assert db_log.status == status
    assert db_log.user_id == user_id
    assert db_log.created_at.year == create_date.year
    assert db_log.created_at.month == create_date.month
    assert db_log.created_at.day == create_date.day


def test_get_log_dao_all_by_category_and_user_id(session, log, monkeypatch):
    """
    Testa a recuperação de logs filtrados por categoria e ID do usuário.

    Verifica se:
        - O retorno não é None.
        - O retorno é uma lista contendo pelo menos um Log.
        - Os elementos da lista são instâncias de Log.
    """

    monkeypatch.setattr(
        'database.dao.log_dao.get_session',
        lambda: session
    )

    db_log = LogDAO.get_all_by_category_and_user_id(log.user_id, log.category)

    assert db_log is not None
    assert isinstance(db_log, list)
    assert len(db_log) > 0
    assert isinstance(db_log[0], Log)


def test_get_log_dao_all_by_color_and_user_id(session, log, monkeypatch):
    """
    Testa a recuperação de logs filtrados por cor e ID do usuário.

    Verifica se:
        - O retorno não é None.
        - O retorno é uma lista contendo pelo menos um Log.
        - Os elementos da lista são instâncias de Log.
    """

    monkeypatch.setattr(
        'database.dao.log_dao.get_session',
        lambda: session
    )

    db_log = LogDAO.get_all_by_color_and_user_id(log.user_id, log.color)

    assert db_log is not None
    assert isinstance(db_log, list)
    assert len(db_log) > 0
    assert isinstance(db_log[0], Log)


def test_get_all_by_status_and_user_id(session, log, monkeypatch):
    """
    Testa a recuperação de logs filtrados por status e ID do usuário.

    Verifica se:
        - O retorno não é None.
        - O retorno é uma lista contendo pelo menos um Log.
        - Os elementos da lista são instâncias de Log.
    """
    monkeypatch.setattr(
        'database.dao.log_dao.get_session',
        lambda: session
    )

    db_log = LogDAO.get_all_by_status_and_user_id(log.user_id, log.status)

    assert db_log is not None
    assert isinstance(db_log, list)
    assert len(db_log) > 0
    assert isinstance(db_log[0], Log)


def test_get_log_dao_all_by_user_id(session, log, monkeypatch):
    """
    Testa a recuperação de todos os logs de um usuário pelo ID.

    Verifica se:
        - O retorno não é None.
    """
    monkeypatch.setattr(
        'database.dao.log_dao.get_session',
        lambda: session
    )
    
    db_log = LogDAO.get_all_by_user_id(log.user_id)

    assert db_log is not None
 
def test_get_last_execution_by_user_id(session, log, monkeypatch):
    """
    Testa a recuperação do último log (última execução) de um usuário.

    Verifica se:
        - O retorno não é None.
    """
    monkeypatch.setattr(
        'database.dao.log_dao.get_session',
        lambda: session
    )

    db_log = LogDAO.get_last_execution_by_user_id(log.user_id)

    assert db_log is not None
    