import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

from src.config import settings
from src.database import Base, get_db
from src.main import app


@pytest.fixture(scope='session')
def db_engine():
    global engine  # noqa
    db_url = f'{settings.db.url}_test'
    engine = create_engine(db_url, future=True)
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(bind=engine)
    else:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope='session', autouse=True)
def get_test_session(db_engine):
    session = sessionmaker(bind=db_engine)()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


@pytest.fixture(scope='session')
def client(get_test_session):
    def override_get_db():
        try:
            yield get_test_session
        finally:
            get_test_session.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
