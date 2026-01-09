from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./careerpilot.db"  # TODO: MVP DB --> change later

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite requirement
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency for providing a transactional scope.
    Usage: Depends(get_session)
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
