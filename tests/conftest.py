import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool
from tests import models
from tests.models import Base


class MockResolveInfo:
    def __init__(self, context):
        self.context = context


@pytest.fixture
def session():
    db = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,
    )
    connection = db.engine.connect()
    transaction = connection.begin()
    Base.metadata.create_all(connection)

    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture
def info():
    db = create_engine("sqlite://")  # in-memory
    connection = db.engine.connect()
    transaction = connection.begin()
    Base.metadata.create_all(connection)

    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)

    yield MockResolveInfo(context={"session": session})

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture
def info_and_user_query():
    db = create_engine("sqlite://")  # in-memory
    connection = db.engine.connect()
    transaction = connection.begin()
    Base.metadata.create_all(connection)

    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)

    info = MockResolveInfo(context={"session": session})
    user_query = session.query(models.User)

    yield info, user_query

    transaction.rollback()
    connection.close()
    session.remove()
