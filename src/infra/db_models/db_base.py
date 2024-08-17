from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker

from configs import config


class DbBase(DeclarativeBase):  # type: ignore
    """Base class for database models."""


engine = create_engine(config.DB_URI)
Session = scoped_session(sessionmaker(bind=engine))
