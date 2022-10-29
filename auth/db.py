import uuid

from sqlalchemy import create_engine, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker

from lib import get_env

__all__ = ["User", "session_maker"]

user = get_env("POSTGRES_USER")
password = get_env("POSTGRES_PASSWORD")
host = get_env("DB_HOST")
port = get_env("DB_PORT")
name = get_env("POSTGRES_DB")
connection_url = f"postgresql://{user}:{password}@{host}:{port}/{name}"

engine = create_engine(connection_url, echo=True, future=True)
session_maker: sessionmaker = sessionmaker(engine)

Base = declarative_base()


class User(Base):
    """Model representing single ToDo item."""  # noqa
    __tablename__ = "User"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(100), nullable=False)

    def __repr__(self):
        return f"User(email={self.email})"
