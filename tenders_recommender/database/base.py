import yaml
from pkg_resources import resource_stream
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CONFIG = resource_stream('backend.tenders_recommender', 'config.yml')
DATABASE_URL = yaml.safe_load(CONFIG).get("database_url")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()
