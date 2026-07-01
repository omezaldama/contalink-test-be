import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_session
from app.db.base import Base


TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"
test_engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_session():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

app.dependency_overrides[get_session] = override_get_session
