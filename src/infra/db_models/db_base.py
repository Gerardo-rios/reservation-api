from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from config import config


class DbBase:
    """Base class for database models."""


engine = create_engine(config.DB_URI)
Session = scoped_session(sessionmaker(bind=engine))
