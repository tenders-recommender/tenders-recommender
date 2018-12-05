import yaml
from pkg_resources import resource_stream
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, scoped_session, Session as SqlAlchemySession

__CONFIG = resource_stream('resources', 'config.yml')
__DATABASE_URL = yaml.safe_load(__CONFIG).get("database_url")
__ENGINE = create_engine(__DATABASE_URL)
__SESSION: scoped_session = scoped_session(sessionmaker(bind=__ENGINE))

Base: DeclarativeMeta = declarative_base()
Base.query = __SESSION.query_property()

Session: SqlAlchemySession = __SESSION


def init_database():
    Base.metadata.create_all(bind=__ENGINE)
