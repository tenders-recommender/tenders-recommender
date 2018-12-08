from sqlalchemy import Column, Integer, JSON
from typing import Dict

from tenders_recommender.database.database_config import Base


class Descriptions(Base):
    __tablename__ = 'descriptions'
    id = Column(Integer, primary_key=True)
    data: Dict[str, str] = Column(JSON)

    def __init__(self, data):
        self.data = data
