# backend/tests/conftest.py
from typing import Callable, Generator

import pytest
from app.core.errors import EntityNotFoundError
from app.db.base import Base
from app.db.session import get_session as real_get_session
from app.main import create_app
from app.models import Company
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from tests.factories.company import create_company

TEST_DATABASE_URL = "sqlite:///:memory:"


# -------------------------
# Database setup
# -------------------------


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        future=True,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def SessionLocal(engine) -> Callable[..., Session]:
    return sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        future=True,
    )


@pytest.fixture(scope="function")
def db_session(engine, SessionLocal) -> Generator[Session, None, None]:
    """
    Provide a transactional scope for each test.
    Each test runs inside a transaction that is rolled back afterward.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


# -------------------------
# FastAPI app + client
# -------------------------


@pytest.fixture
def app(db_session) -> Generator:
    """
    Create the real FastAPI app via create_app(), then override the DB dependency
    so request handlers use the test session instance.
    """
    app = create_app()

    def override_get_session():
        try:
            yield db_session
        finally:
            pass

    # Override the dependency used by the routers
    app.dependency_overrides[real_get_session] = override_get_session

    # Ensure the EntityNotFoundError handler is registered
    handler = app.exception_handlers.get(EntityNotFoundError)
    assert handler is not None, "EntityNotFoundError handler not registered on app"

    yield app

    # Clean overrides after test
    app.dependency_overrides.clear()


@pytest.fixture
def client(app):
    return TestClient(app)


# -------------------------
# Factories
# -------------------------


@pytest.fixture
def company_factory(db_session):
    return lambda **kwargs: create_company(db_session, **kwargs)
