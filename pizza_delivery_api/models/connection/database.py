from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .secrets import connection_uri

engine = create_engine(connection_uri, echo=True)

Base = declarative_base()
Session = sessionmaker()
