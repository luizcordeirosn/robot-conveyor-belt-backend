from sqlalchemy import select
from database.model.log import Log

def test_log_model_creation(session):
    """
    Testa a criação de uma instância do modelo Log.

    Verifica se:
        - O nome da tabela do modelo é 'logs'.
        - Os campos (category, color, status, user_id) são atribuídos corretamente.
        - O ID é gerado como um inteiro após adicionar e commitar no banco de dados.
    """
    assert Log.__tablename__ == 'logs'

    new_log = Log(
        category='reciclável',
        color='verde',
        status='OK',
        user_id=1
    )

    session.add(new_log)
    session.commit()
    session.refresh(new_log)

    assert isinstance(new_log.id, int)
    assert new_log.category == 'reciclável'
    assert new_log.color == 'verde'
    assert new_log.status == 'OK'
    assert new_log.user_id == 1

def test_log_model_selected(session, log):
    """
    Testa a recuperação de uma instância de Log do banco de dados.

    Verifica se:
        - O log recuperado não é None.
        - Os campos (category, color, status, user_id) correspondem aos valores esperados.
        - A data de criação (created_at) está presente e é consistente com o log original.
    """
    db_log = session.scalar(
        select(Log).where(Log.id == log.id)
    )

    assert db_log is not None
    assert db_log.category == log.category
    assert db_log.color == log.color
    assert db_log.status == log.status
    assert db_log.user_id == log.user_id
    assert db_log.created_at == log.created_at
 

    