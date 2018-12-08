from sqlalchemy import Column, Integer, JSON, String

from tenders_recommender.database.database_config import Base


class TestResults(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    results = Column(JSON)

    def __init__(self, type, results):
        self.type = type
        self.results = results
