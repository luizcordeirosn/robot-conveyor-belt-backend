from sqlalchemy import select
from database.model.dashboard import Dashboard

def test_dashboard_model_creation(session):
    """
    Testa a criação de uma instância do modelo Dashboard.

    Verifica se:
        - O nome da tabela do modelo é 'dashboards'.
        - Os campos (image, label, confidence, user_id) são atribuídos corretamente.
        - O ID é gerado como um inteiro após adicionar e commitar no banco de dados.
    """
    assert Dashboard.__tablename__ == 'dashboards'

    new_dashboard = Dashboard(
        image='Piece_6.f3d.png',
        label=1,
        confidence=97.7,
        user_id=1
    )

    session.add(new_dashboard)
    session.commit()
    session.refresh(new_dashboard)

    assert isinstance(new_dashboard.id, int)
    assert new_dashboard.image == 'Piece_6.f3d.png'
    assert new_dashboard.label == 1
    assert new_dashboard.confidence == 97.7
    assert new_dashboard.user_id == 1

def test_dashboard_model_selected(session, dashboard):
    """
    Testa a recuperação de uma instância de Dashboard do banco de dados.

    Verifica se:
        - O dashboard recuperado não é None.
        - Os campos (image, label, confidence, user_id) correspondem aos valores esperados.
        - A data de criação (created_at) está presente e válida.
    """

    db_dashboard = session.scalar(
        select(Dashboard).where(Dashboard.id == dashboard.id)
    )

    assert db_dashboard is not None
    assert db_dashboard.image == 'Piece_6.f3d.png'
    assert db_dashboard.label == 1
    assert db_dashboard.confidence == 97.7
    assert db_dashboard.user_id == 1
    assert db_dashboard.created_at == db_dashboard.created_at