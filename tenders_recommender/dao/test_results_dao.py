from tenders_recommender.database import Session
from tenders_recommender.model import TestResults


class TestResultsDao(object):

    @staticmethod
    def insert_results(test_results: TestResults) -> None:
        Session.add(test_results)
        Session.commit()

    @staticmethod
    def query_results(type: str):
        json = Session.query(TestResults).filter_by(type=type).order_by(TestResults.id.desc()).first()
        return json.results
