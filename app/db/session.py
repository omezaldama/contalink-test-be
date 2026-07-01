from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings


database_url = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_host}:5432/{settings.db_database}'

engine = create_engine(
    database_url,
    echo=False,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session, Any, None]:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
