import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import yaml

CONFIG_PATH: str = os.path.join('..', '..', '..', '.config.yml')

DATABASE_URL = yaml.safe_load(open(CONFIG_PATH)).get("database_url")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()
