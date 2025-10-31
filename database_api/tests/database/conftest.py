import pytest

from database.model.user import User
from database.model.log import Log
from database.model.dashboard import Dashboard

from database.dao.user_dao import UserDAO

@pytest.fixture
def user(session):
    """Creates a new user for testing"""
    new_user = User(
        name='test',
        username='testuser',
        password='test123',
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@pytest.fixture
def log(session):
    """Creates a new log for testing"""
    new_log = Log(
        category='reciclável',
        color='verde',
        status='OK',
        user_id=1
    )

    session.add(new_log)
    session.commit()
    session.refresh(new_log)

    return new_log

@pytest.fixture
def dashboard(session):
    """Creates a new dashboard for testing"""
    new_dashboard = Dashboard(
        image='Piece_6.f3d.png',
        label=1,
        confidence=97.7,
        user_id=1
    )
    
    session.add(new_dashboard)
    session.commit()
    session.refresh(new_dashboard)

    return new_dashboard

#fixture para testar user em rota
@pytest.fixture
def test_user_route(session):
    new_user = User(
        name='admin',
        username='admin',
        password='admin123',
    )

    yield UserDAO.create(new_user).as_dict()

    new_user = User(
        name='guest',
        username='guest',
        password='guest123',
    )
    UserDAO.create(new_user)