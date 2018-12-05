from typing import List

from sqlalchemy import Column, Integer, JSON

from tenders_recommender.database.database_config import Base
from .types import Interaction


class UsersInteractions(Base):
    __tablename__ = 'users_interactions'
    id = Column(Integer, primary_key=True)
    users_interactions = Column(JSON)

    def __init__(self, users_interactions: List[Interaction]):
        self.users_interactions = users_interactions
