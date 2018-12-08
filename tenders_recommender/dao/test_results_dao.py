from tenders_recommender.database import Session
from tenders_recommender.model import TestResults, ResultTypes


class TestResultsDao(object):

    @staticmethod
    def insert_results(test_results: TestResults) -> None:
        Session.add(test_results)
        Session.commit()

    @staticmethod
    def query_results(type: str):
        result_type = ResultTypes.types[type]
        json = Session.query(TestResults).filter_by(type=result_type).order_by(TestResults.id.desc()).first()
        return json.results
