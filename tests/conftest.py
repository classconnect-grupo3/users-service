import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.db import Base

# Usar la URL de DATABASE_URL desde .env.test
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5433/test_db"
)

# Para tests necesitamos usar psycopg2 en lugar de asyncpg
# porque pytest-asyncio no maneja bien las conexiones async en fixtures
TEST_DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql")


@pytest.fixture(scope="session")
def db_engine():
    """Create a SQLAlchemy engine for the test database."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a new database session for each test."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
