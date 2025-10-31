from datetime import datetime
from database.dao.dashboard_dao import DashboardDAO
from database.model.dashboard import Dashboard

def test_dashboard_dao_create(session, monkeypatch):
    """
    Testa a criação de um novo dashboard no banco de dados.

    Verifica se:
        - O dashboard recebe um ID após ser criado.
        - Todos os campos (image, label, confidence, user_id) são salvos corretamente.
        - A data de criação (created_at) corresponde ao dia atual.
    """
    
    monkeypatch.setattr(
        'database.dao.dashboard_dao.get_session',
        lambda: session
    )
    
    image = 'Piece_6.f3d.png'
    new_dashboard = Dashboard(
        image='Piece_6.f3d.png',
        label=1,
        confidence=97.7,
        user_id=1
    )

    db_dashboard = DashboardDAO.create(new_dashboard)
    create_date = datetime.now()

    assert db_dashboard.id is not None
    assert db_dashboard.image == image
    assert db_dashboard.label == 1
    assert db_dashboard.confidence == 97.7
    assert db_dashboard.user_id == 1
    assert db_dashboard.created_at.year == create_date.year
    assert db_dashboard.created_at.month == create_date.month
    assert db_dashboard.created_at.day == create_date.day

def test_get_dashboard_dao_all_by_user_id(session, dashboard, monkeypatch):
    """
    Testa a recuperação de dashboards pelo ID do usuário.

    Verifica se:
        - O retorno não é None.
        - O retorno é uma lista.
        - A lista contém ao menos um dashboard.
        - Os elementos da lista são instâncias de Dashboard.
    """
    monkeypatch.setattr(
        'database.dao.dashboard_dao.get_session',
        lambda: session
    )

    db_dashboard = DashboardDAO.get_all_by_user_id(dashboard.user_id)

    assert db_dashboard is not None
    assert isinstance(db_dashboard, list)
    assert len(db_dashboard) > 0
    assert isinstance(db_dashboard[0], Dashboard)


def test_get_dashboard_dao_all_by_label_and_user_id(session, dashboard, monkeypatch):
    """
    Testa a recuperação de dashboards pelo ID do usuário e pelo label.

    Verifica se:
        - O retorno não é None.
        - O retorno é uma lista.
        - A lista contém ao menos um dashboard.
        - Os elementos da lista são instâncias de Dashboard.
    """

    monkeypatch.setattr(
        'database.dao.log_dao.get_session',
        lambda: session
    )

    db_dashboard= DashboardDAO.get_all_by_label_and_user_id(dashboard.user_id, dashboard.label)

    assert db_dashboard is not None
    assert isinstance(db_dashboard, list)
    assert len(db_dashboard) > 0
    assert isinstance(db_dashboard[0], Dashboard)
