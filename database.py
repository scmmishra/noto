from sqlmodel import Session, SQLModel

from settings import Config


def create_db_and_tables():
    """Create database and tables"""
    SQLModel.metadata.create_all(Config.engine)


def get_session():
    """Yie;d a new session"""
    with Session(Config.engine) as session:
        yield session
