from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

from .secrets import Settings

settings = Settings()

engine = create_engine(settings.DATABASE_URL)

Base = declarative_base()


def get_session():
    with Session(engine) as session:
        yield session
